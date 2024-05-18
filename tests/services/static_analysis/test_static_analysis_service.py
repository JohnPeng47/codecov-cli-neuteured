from asyncio import CancelledError
from pathlib import Path
from unittest.mock import MagicMock

import click
import httpx
import pytest
import requests
import responses
from responses import matchers

from codecov_cli.services.staticanalysis import (
    process_files,
    run_analysis_entrypoint,
    send_single_upload_put,
)
from codecov_cli.services.staticanalysis.types import (
    FileAnalysisRequest,
    FileAnalysisResult,
)


class TestStaticAnalysisService:








    @pytest.mark.asyncio
    async def test_static_analysis_service_should_force_option(self, mocker):
        mock_file_finder = mocker.patch(
            "codecov_cli.services.staticanalysis.select_file_finder"
        )
        mock_send_upload_put = mocker.patch(
            "codecov_cli.services.staticanalysis.send_single_upload_put"
        )

        # Doing it this way to support Python 3.7
        async def side_effect(*args, **kwargs):
            return MagicMock()

        mock_send_upload_put.side_effect = side_effect

        files_found = map(
            lambda filename: FileAnalysisRequest(str(filename), Path(filename)),
            [
                "samples/inputs/sample_001.py",
                "samples/inputs/sample_002.py",
            ],
        )
        mock_file_finder.return_value.find_files = MagicMock(return_value=files_found)
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://api.codecov.io/staticanalysis/analyses",
                json={
                    "external_id": "externalid",
                    "filepaths": [
                        {
                            "state": "created",
                            "filepath": "samples/inputs/sample_001.py",
                            "raw_upload_location": "http://storage-url",
                        },
                        {
                            "state": "valid",
                            "filepath": "samples/inputs/sample_002.py",
                            "raw_upload_location": "http://storage-url",
                        },
                    ],
                },
                status=200,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            rsps.add(
                responses.POST,
                "https://api.codecov.io/staticanalysis/analyses/externalid/finish",
                status=204,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            await run_analysis_entrypoint(
                config={},
                folder=".",
                numberprocesses=1,
                pattern="*.py",
                token="STATIC_TOKEN",
                commit="COMMIT",
                should_force=True,
                folders_to_exclude=[],
                enterprise_url=None,
            )
        mock_file_finder.assert_called_with({})
        mock_file_finder.return_value.find_files.assert_called()
        assert mock_send_upload_put.call_count == 2

    @pytest.mark.asyncio
    async def test_static_analysis_service_no_upload(self, mocker):
        mock_file_finder = mocker.patch(
            "codecov_cli.services.staticanalysis.select_file_finder"
        )
        mock_send_upload_put = mocker.patch(
            "codecov_cli.services.staticanalysis.send_single_upload_put"
        )

        # Doing it this way to support Python 3.7
        async def side_effect(*args, **kwargs):
            return MagicMock()

        mock_send_upload_put.side_effect = side_effect

        files_found = map(
            lambda filename: FileAnalysisRequest(str(filename), Path(filename)),
            [
                "samples/inputs/sample_001.py",
                "samples/inputs/sample_002.py",
            ],
        )
        mock_file_finder.return_value.find_files = MagicMock(return_value=files_found)
        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://api.codecov.io/staticanalysis/analyses",
                json={
                    "external_id": "externalid",
                    "filepaths": [
                        {
                            "state": "valid",
                            "filepath": "samples/inputs/sample_001.py",
                            "raw_upload_location": "http://storage-url",
                        },
                        {
                            "state": "valid",
                            "filepath": "samples/inputs/sample_002.py",
                            "raw_upload_location": "http://storage-url",
                        },
                    ],
                },
                status=200,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            rsps.add(
                responses.POST,
                "https://api.codecov.io/staticanalysis/analyses/externalid/finish",
                status=204,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )

            await run_analysis_entrypoint(
                config={},
                folder=".",
                numberprocesses=1,
                pattern="*.py",
                token="STATIC_TOKEN",
                commit="COMMIT",
                should_force=False,
                folders_to_exclude=[],
                enterprise_url=None,
            )
        mock_file_finder.assert_called_with({})
        mock_file_finder.return_value.find_files.assert_called()
        assert mock_send_upload_put.call_count == 0
