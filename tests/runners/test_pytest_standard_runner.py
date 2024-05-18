from subprocess import CalledProcessError
from unittest.mock import MagicMock, call, patch

import click
import pytest
from pytest import ExitCode

from codecov_cli.runners.pytest_standard_runner import (
    PytestStandardRunner,
    PytestStandardRunnerConfigParams,
)
from codecov_cli.runners.pytest_standard_runner import logger as runner_logger
from codecov_cli.runners.pytest_standard_runner import stdout as pyrunner_stdout
from codecov_cli.runners.types import LabelAnalysisRequestResult


class TestPythonStandardRunner(object):
    runner = PytestStandardRunner()


    @patch("codecov_cli.runners.pytest_standard_runner.subprocess")

    @patch("codecov_cli.runners.pytest_standard_runner.logger.warning")


    @patch("codecov_cli.runners.pytest_standard_runner.subprocess")

    @patch("codecov_cli.runners.pytest_standard_runner.subprocess")






    def test_process_label_analysis_result_with_options(self, mocker):
        label_analysis_result = {
            "present_report_labels": ["test_present"],
            "absent_labels": ["test_absent"],
            "present_diff_labels": ["test_in_diff"],
            "global_level_labels": ["test_global"],
        }
        mock_execute = mocker.patch.object(PytestStandardRunner, "_execute_pytest")
        mock_warning = mocker.patch.object(runner_logger, "warning")

        runner_config = {
            "execute_tests_options": ["-s", "--cov-report=xml", "--cov=something"]
        }
        runner = PytestStandardRunner(runner_config)
        runner.process_labelanalysis_result(
            LabelAnalysisRequestResult(label_analysis_result)
        )
        args, kwargs = mock_execute.call_args
        assert kwargs == {"capture_output": False}
        assert isinstance(args[0], list)
        actual_command = args[0]
        assert actual_command[:5] == [
            "--cov=./",
            "--cov-context=test",
            "-s",
            "--cov-report=xml",
            "--cov=something",
        ]
        assert sorted(actual_command[5:]) == [
            "test_absent",
            "test_global",
            "test_in_diff",
        ]
        # The --cov option should trigger a warning
        mock_warning.assert_called_with(
            "--cov option detected when running tests. Please use coverage_root config option instead"
        )

    def test_process_label_analysis_skip_all_tests(self, mocker):
        label_analysis_result = {
            "present_report_labels": ["test_present"],
            "absent_labels": [],
            "present_diff_labels": [],
            "global_level_labels": [],
        }
        mock_execute = mocker.patch.object(PytestStandardRunner, "_execute_pytest")

        self.runner.process_labelanalysis_result(
            LabelAnalysisRequestResult(label_analysis_result)
        )
        args, kwargs = mock_execute.call_args
        assert kwargs == {"capture_output": False}
        assert isinstance(args[0], list)
        actual_command = args[0]
        assert actual_command[:2] == [
            "--cov=./",
            "--cov-context=test",
        ]
        assert sorted(actual_command[2:]) == [
            "test_present",
        ]
