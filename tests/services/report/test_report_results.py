import uuid
from unittest.mock import patch

from click.testing import CliRunner

from codecov_cli.services.report import (
    create_report_results_logic,
    send_reports_result_get_request,
    send_reports_result_request,
)
from codecov_cli.types import RequestError, RequestResult, RequestResultWarning
from tests.test_helpers import parse_outstreams_into_log_lines












@patch("codecov_cli.services.report.MAX_NUMBER_TRIES", 1)




def test_get_report_results_200_undefined_state(mocker, capsys):
    mocked_response = mocker.patch(
        "codecov_cli.services.report.requests.get",
        return_value=mocker.MagicMock(
            status_code=200, text='{"state": "undefined_state", "result": {}}'
        ),
    )
    token = uuid.uuid4()
    res = send_reports_result_get_request(
        "commit_sha", "report_code", "encoded_slug", "service", token, None
    )
    output = parse_outstreams_into_log_lines(capsys.readouterr().err)
    assert res.error is None
    assert res.warnings == []
    mocked_response.assert_called_once()
    assert ("error", "Please try again later.") in output


def test_get_report_results_401(mocker, capsys):
    mocked_response = mocker.patch(
        "codecov_cli.services.report.requests.get",
        return_value=mocker.MagicMock(
            status_code=401, text='{"detail": "Invalid token."}'
        ),
    )
    token = uuid.uuid4()
    res = send_reports_result_get_request(
        "commit_sha", "report_code", "encoded_slug", "service", token, None
    )
    output = parse_outstreams_into_log_lines(capsys.readouterr().err)
    assert res.error == RequestError(
        code="HTTP Error 401",
        description='{"detail": "Invalid token."}',
        params={},
    )
    mocked_response.assert_called_once()
    assert (
        "error",
        'Getting report results failed: {"detail": "Invalid token."}',
    ) in output
