import json
import uuid

from click.testing import CliRunner

from codecov_cli.services.empty_upload import empty_upload_logic
from codecov_cli.types import RequestError, RequestResult, RequestResultWarning
from tests.test_helpers import parse_outstreams_into_log_lines








def test_empty_upload_403(mocker):
    mocked_response = mocker.patch(
        "codecov_cli.helpers.request.requests.post",
        return_value=mocker.MagicMock(status_code=403, text="Permission denied"),
    )
    token = uuid.uuid4()
    res = empty_upload_logic(
        "commit_sha", "owner/repo", token, "service", None, False, False
    )
    assert res.error == RequestError(
        code="HTTP Error 403",
        description="Permission denied",
        params={},
    )
    mocked_response.assert_called_once()


def test_empty_upload_force(mocker):
    res = {
        "result": "Force option was enabled. Triggering passing notifications.",
        "non_ignored_files": [],
    }
    mocked_response = mocker.patch(
        "codecov_cli.helpers.request.requests.post",
        return_value=RequestResult(
            status_code=200, error=None, warnings=[], text=json.dumps(res)
        ),
    )
    token = uuid.uuid4()
    runner = CliRunner()
    with runner.isolation() as outstreams:
        res = empty_upload_logic(
            "commit_sha", "owner/repo", token, "service", None, False, True
        )
    out_bytes = parse_outstreams_into_log_lines(outstreams[0].getvalue())
    assert out_bytes == [
        ("info", "Process Empty Upload complete"),
        ("info", "Force option was enabled. Triggering passing notifications."),
        ("info", "Non ignored files []"),
    ]
    assert res.error is None
    assert res.warnings == []
    mocked_response.assert_called_once()
