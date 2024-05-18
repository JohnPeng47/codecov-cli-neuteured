import json
import uuid

from click.testing import CliRunner

from codecov_cli.services.upload_completion import upload_completion_logic
from codecov_cli.types import RequestError, RequestResult, RequestResultWarning
from tests.test_helpers import parse_outstreams_into_log_lines






def test_upload_completion_200(mocker):
    res = {
        "uploads_total": 2,
        "uploads_success": 2,
        "uploads_processing": 0,
        "uploads_error": 0,
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
        res = upload_completion_logic(
            "commit_sha", "owner/repo", token, "service", None
        )
    out_bytes = parse_outstreams_into_log_lines(outstreams[0].getvalue())
    assert out_bytes == [
        ("info", "Process Upload Completion complete"),
        (
            "info",
            "{'uploads_total': 2, 'uploads_success': 2, 'uploads_processing': 0, 'uploads_error': 0}",
        ),
    ]
    assert res.error is None
    assert res.warnings == []
    mocked_response.assert_called_once()


def test_upload_completion_403(mocker):
    mocked_response = mocker.patch(
        "codecov_cli.helpers.request.requests.post",
        return_value=mocker.MagicMock(status_code=403, text="Permission denied"),
    )
    token = uuid.uuid4()
    res = upload_completion_logic("commit_sha", "owner/repo", token, "service", None)
    assert res.error == RequestError(
        code="HTTP Error 403",
        description="Permission denied",
        params={},
    )
    mocked_response.assert_called_once()
