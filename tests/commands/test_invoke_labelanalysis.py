import json
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

import click
import pytest
import responses
from click.testing import CliRunner
from responses import matchers

from codecov_cli.commands.labelanalysis import (
    _dry_run_json_output,
    _dry_run_list_output,
    _fallback_to_collected_labels,
    _parse_runner_params,
    _potentially_calculate_absent_labels,
    _send_labelanalysis_request,
)
from codecov_cli.commands.labelanalysis import time as labelanalysis_time
from codecov_cli.main import cli
from codecov_cli.runners.types import LabelAnalysisRequestResult
from tests.factory import FakeProvider, FakeRunner, FakeVersioningSystem


@pytest.fixture
def fake_ci_provider():
    return FakeProvider()


@pytest.fixture
def get_labelanalysis_deps(mocker):
    fake_ci_provider = FakeProvider()
    fake_versioning_system = FakeVersioningSystem()
    collected_labels = [
        "test_present",
        "test_absent",
        "test_in_diff",
        "test_global",
    ]
    fake_runner = FakeRunner(collect_tests_response=collected_labels)
    fake_runner.process_labelanalysis_result = mocker.MagicMock()

    mocker.patch.object(labelanalysis_time, "sleep")
    mocker.patch("codecov_cli.main.get_ci_adapter", return_value=fake_ci_provider)
    mocker.patch(
        "codecov_cli.main.get_versioning_system",
        return_value=fake_versioning_system,
    )
    mock_get_runner = mocker.patch(
        "codecov_cli.commands.labelanalysis.get_runner", return_value=fake_runner
    )
    return {
        "mock_get_runner": mock_get_runner,
        "fake_runner": fake_runner,
        "collected_labels": collected_labels,
    }


FAKE_BASE_SHA = "0111111111111111111111111111111111111110"


class TestLabelAnalysisNotInvoke(object):




    def test__dry_run_space_separated_list_output(self):
        list_to_run = ["label_1", "label_2"]
        list_to_skip = ["label_3", "label_4"]
        runner_options = ["--option=1", "--option=2"]

        with StringIO() as out:
            with redirect_stdout(out):
                _dry_run_list_output(
                    labels_to_run=list_to_run,
                    labels_to_skip=list_to_skip,
                    runner_options=runner_options,
                )
                stdout = out.getvalue()

        assert (
            stdout
            == "TESTS_TO_RUN='--option=1' '--option=2' 'label_1' 'label_2'\nTESTS_TO_SKIP='--option=1' '--option=2' 'label_3' 'label_4'\n"
        )

    def test_parse_dynamic_runner_options(self):
        params = [
            "wrong_param",
            "key=value",
            "list_key=val1,val2,val3",
            "point=somethingwith=sign",
        ]
        assert _parse_runner_params(params) == {
            "wrong_param": None,
            "key": "value",
            "list_key": ["val1", "val2", "val3"],
            "point": "somethingwith=sign",
        }


class TestLabelAnalysisCommand(object):













    def test_fallback_collected_labels_codecov_max_wait_time_exceeded_dry_run(
        self, get_labelanalysis_deps, mocker, use_verbose_option
    ):
        mock_get_runner = get_labelanalysis_deps["mock_get_runner"]
        fake_runner = get_labelanalysis_deps["fake_runner"]
        collected_labels = get_labelanalysis_deps["collected_labels"]
        mocker.patch.object(labelanalysis_time, "monotonic", side_effect=[0, 6])

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://api.codecov.io/labels/labels-analysis",
                json={"external_id": "label-analysis-request-id"},
                status=201,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            rsps.add(
                responses.PATCH,
                "https://api.codecov.io/labels/labels-analysis/label-analysis-request-id",
                json={"external_id": "label-analysis-request-id"},
                status=201,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            rsps.add(
                responses.GET,
                "https://api.codecov.io/labels/labels-analysis/label-analysis-request-id",
                json={"state": "processing"},
            )
            cli_runner = CliRunner(mix_stderr=False)
            result = cli_runner.invoke(
                cli,
                [
                    "label-analysis",
                    "--token=STATIC_TOKEN",
                    f"--base-sha={FAKE_BASE_SHA}",
                    "--max-wait-time=5",
                    "--dry-run",
                ],
                obj={},
            )
            mock_get_runner.assert_called()
            fake_runner.process_labelanalysis_result.assert_not_called()
        # Dry run format defaults to json
        assert json.loads(result.stdout) == {
            "runner_options": ["--labels"],
            "ats_tests_to_run": sorted(collected_labels),
            "ats_tests_to_skip": [],
            "ats_fallback_reason": "max_wait_time_exceeded",
        }
        assert result.exit_code == 0

    def test_first_labelanalysis_request_fails_but_second_works(
        self, get_labelanalysis_deps, mocker, use_verbose_option
    ):
        mock_get_runner = get_labelanalysis_deps["mock_get_runner"]
        fake_runner = get_labelanalysis_deps["fake_runner"]
        collected_labels = get_labelanalysis_deps["collected_labels"]

        label_analysis_result = {
            "present_report_labels": ["test_present"],
            "absent_labels": ["test_absent"],
            "present_diff_labels": ["test_in_diff"],
            "global_level_labels": ["test_global"],
        }

        with responses.RequestsMock() as rsps:
            rsps.add(
                responses.POST,
                "https://api.codecov.io/labels/labels-analysis",
                status=502,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            rsps.add(
                responses.POST,
                "https://api.codecov.io/labels/labels-analysis",
                json={"external_id": "label-analysis-request-id"},
                status=201,
                match=[
                    matchers.header_matcher({"Authorization": "Repotoken STATIC_TOKEN"})
                ],
            )
            rsps.add(
                responses.GET,
                "https://api.codecov.io/labels/labels-analysis/label-analysis-request-id",
                json={"state": "finished", "result": label_analysis_result},
            )
            cli_runner = CliRunner()
            result = cli_runner.invoke(
                cli,
                [
                    "label-analysis",
                    "--token=STATIC_TOKEN",
                    f"--base-sha={FAKE_BASE_SHA}",
                ],
                obj={},
            )
            assert result.exit_code == 0
        mock_get_runner.assert_called()
        fake_runner.process_labelanalysis_result.assert_called_with(
            label_analysis_result
        )
        print(result.output)
