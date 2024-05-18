from urllib import parse

import pytest
import responses
from responses import matchers

from codecov_cli import __version__ as codecov_cli_version
from codecov_cli.services.upload.legacy_upload_sender import LegacyUploadSender
from codecov_cli.types import UploadCollectionResult
from tests.data import reports_examples

upload_collection = UploadCollectionResult(["1", "apple.py", "3"], [], [])
random_token = "f359afb9-8a2a-42ab-a448-c3d267ff495b"
random_sha = "845548c6b95223f12e8317a1820705f64beaf69e"
named_upload_data = {
    "name": "name",
    "branch": "branch",
    "slug": "slug",
    "pull_request_number": "pr",
    "build_code": "build_code",
    "build_url": "build_url",
    "job_code": "job_code",
    "flags": "flags",
    "ci_service": "ci_service",
    "git_service": "git_service",
}


@pytest.fixture
def mocked_responses():
    with responses.RequestsMock() as rsps:
        yield rsps


@pytest.fixture
def mocked_legacy_upload_endpoint(mocked_responses):
    resp = responses.Response(
        responses.POST,
        "https://codecov.io/upload/v4",
        body="https://resulturl.com\nhttps://puturl.com",
        status=200,
    )
    mocked_responses.add(resp)
    yield resp


@pytest.fixture
def mocked_legacy_upload_endpoint_too_many_fails(mocked_responses):
    resp = responses.Response(
        responses.POST,
        "https://codecov.io/upload/v4",
        body="https://resulturl.com\nhttps://puturl.com",
        status=400,
    )
    for _ in range(4):
        mocked_responses.add(resp)


@pytest.fixture
def mocked_storage_server(mocked_responses):
    resp = responses.Response(responses.PUT, "https://puturl.com", status=200)
    mocked_responses.add(resp)
    yield resp


class TestUploadSender(object):




    def test_upload_sender_result_fail_put_400(
        self, mocked_responses, mocked_legacy_upload_endpoint, mocked_storage_server
    ):
        mocked_storage_server.status = 400

        sender = LegacyUploadSender().send_upload_data(
            upload_collection, random_sha, random_token, {}, **named_upload_data
        )

        assert len(mocked_responses.calls) == 2
        assert sender.error is not None
        assert "400" in sender.error.code

        assert sender.warnings is not None

    def test_upload_sender_http_error_with_invalid_sha(
        self, mocked_responses, mocked_legacy_upload_endpoint
    ):
        random_sha = "invalid"

        mocked_legacy_upload_endpoint.body = "Invalid request parameters"
        mocked_legacy_upload_endpoint.status = 400

        sender = LegacyUploadSender().send_upload_data(
            upload_collection,
            random_sha,
            random_token,
            {},
            **named_upload_data,
        )

        assert sender.error is not None
        assert "HTTP Error 400" in sender.error.code
        assert "Invalid request parameters" in sender.error.description


class TestPayloadGeneration(object):





    def test_generate_coverage_files_section(self, mocker):
        mocker.patch(
            "codecov_cli.services.upload.LegacyUploadSender._format_coverage_file",
            side_effect=lambda file_bytes: file_bytes,
        )

        coverage_files = [
            reports_examples.coverage_file_section_simple,
            reports_examples.coverage_file_section_simple,
            reports_examples.coverage_file_section_small,
            reports_examples.coverage_file_section_simple,
        ]

        actual_section = LegacyUploadSender()._generate_coverage_files_section(
            UploadCollectionResult([], coverage_files, [])
        )

        expected_section = b"".join(coverage_files)

        assert actual_section == expected_section

    def test_generate_payload_overall(self, mocker):
        mocker.patch(
            "codecov_cli.services.upload.LegacyUploadSender._generate_env_vars_section",
            return_value=reports_examples.env_section,
        )
        mocker.patch(
            "codecov_cli.services.upload.LegacyUploadSender._generate_network_section",
            return_value=reports_examples.network_section,
        )
        mocker.patch(
            "codecov_cli.services.upload.LegacyUploadSender._generate_coverage_files_section",
            return_value=reports_examples.coverage_file_section_simple,
        )

        actual_report = LegacyUploadSender()._generate_payload(None, None)

        assert actual_report == reports_examples.env_network_coverage_sections
