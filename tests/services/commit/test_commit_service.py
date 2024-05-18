import json
import uuid

import requests
from click.testing import CliRunner
from requests import Response

from codecov_cli.services.commit import create_commit_logic, send_commit_data
from codecov_cli.types import RequestError, RequestResult, RequestResultWarning
from tests.test_helpers import parse_outstreams_into_log_lines








def test_commit_sender_403(mocker):
    mocked_response = mocker.patch(
        "codecov_cli.helpers.request.requests.post",
        return_value=mocker.MagicMock(status_code=403, text="Permission denied"),
    )
    token = uuid.uuid4()
    res = send_commit_data(
        "commit_sha",
        "parent_sha",
        "pr",
        "branch",
        "owner::::repo",
        token,
        "service",
        None,
    )
    assert res.error == RequestError(
        code="HTTP Error 403",
        description="Permission denied",
        params={},
    )
    mocked_response.assert_called_once()


def test_commit_sender_with_forked_repo(mocker):
    mocked_response = mocker.patch(
        "codecov_cli.services.commit.send_post_request",
        return_value=mocker.MagicMock(status_code=200, text="success"),
    )

    def mock_request(*args, headers={}, **kwargs):
        assert headers["X-GitHub-Api-Version"] == "2022-11-28"
        res = {
            "url": "https://api.github.com/repos/codecov/codecov-cli/pulls/1",
            "head": {
                "sha": "123",
                "label": "codecov-cli:branch",
                "ref": "branch",
                "repo": {"full_name": "user_forked_repo/codecov-cli"},
            },
            "base": {
                "sha": "123",
                "label": "codecov-cli:main",
                "ref": "main",
                "repo": {"full_name": "codecov/codecov-cli"},
            },
        }
        response = Response()
        response.status_code = 200
        response._content = json.dumps(res).encode("utf-8")
        return response

    mocker.patch.object(
        requests,
        "get",
        side_effect=mock_request,
    )
    res = send_commit_data(
        "commit_sha",
        "parent_sha",
        "1",
        "branch",
        "codecov::::codecov-cli",
        None,
        "github",
        None,
    )
    mocked_response.assert_called_with(
        url="https://api.codecov.io/upload/github/codecov::::codecov-cli/commits",
        data={
            "commitid": "commit_sha",
            "parent_commit_id": "parent_sha",
            "pullid": "1",
            "branch": "user_forked_repo/codecov-cli:branch",
        },
        headers={"X-Tokenless": "user_forked_repo/codecov-cli", "X-Tokenless-PR": "1"},
    )
