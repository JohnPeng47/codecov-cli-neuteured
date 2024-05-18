import json

import pytest
import requests
from requests import Response

from codecov_cli.helpers import git
from codecov_cli.helpers.git_services.github import Github














def test_pr_is_fork_pr(mocker):
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
    pull_dict = git.get_pull("github", "codecov/codecov-cli", 1)
    assert git.is_fork_pr(pull_dict)


def test_pr_not_found(mocker):
    def mock_request(*args, headers={}, **kwargs):
        assert headers["X-GitHub-Api-Version"] == "2022-11-28"
        response = Response()
        response.status_code = 404
        response._content = b"not-found"
        return response

    mocker.patch.object(
        requests,
        "get",
        side_effect=mock_request,
    )
    pull_dict = git.get_pull("github", "codecov/codecov-cli", 1)
    assert not git.is_fork_pr(pull_dict)
