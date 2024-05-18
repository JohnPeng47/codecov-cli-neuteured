import uuid

import pytest
import requests
from requests import Response

from codecov_cli import __version__
from codecov_cli.helpers.request import (
    get,
    get_token_header_or_fail,
    log_warnings_and_errors_if_any,
)
from codecov_cli.helpers.request import logger as req_log
from codecov_cli.helpers.request import (
    patch,
    request_result,
    send_post_request,
    send_put_request,
)
from codecov_cli.types import RequestError, RequestResult


@pytest.fixture
def valid_response():
    valid_response = Response()
    valid_response.status_code = 200
    valid_response._content = b"response text"
    return valid_response










def test_request_retry_too_many_errors(mocker):
    mock_sleep = mocker.patch("codecov_cli.helpers.request.sleep")
    mocker.patch.object(
        requests,
        "post",
        side_effect=[
            requests.exceptions.ConnectionError(),
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
            requests.exceptions.Timeout(),
        ],
    )
    with pytest.raises(Exception) as exp:
        resp = send_post_request("my_url")
    assert str(exp.value) == "Request failed after too many retries"


def test_user_agent(mocker):
    def mock_request(*args, headers={}, **kwargs):
        assert headers["User-Agent"] == f"codecov-cli/{__version__}"
        return RequestResult(status_code=200, error=None, warnings=[], text="")

    mocker.patch.object(
        requests,
        "post",
        side_effect=mock_request,
    )
    send_post_request("my_url")

    mocker.patch.object(
        requests,
        "get",
        side_effect=mock_request,
    )
    get("my_url")

    mocker.patch.object(
        requests,
        "put",
        side_effect=mock_request,
    )
    send_put_request("my_url")

    mocker.patch.object(
        requests,
        "patch",
        side_effect=mock_request,
    )
    patch("my_url")
