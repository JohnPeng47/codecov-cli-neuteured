from unittest.mock import patch

import pytest

from codecov_cli.runners import _load_runner_from_yaml, get_runner
from codecov_cli.runners.dan_runner import DoAnythingNowRunner
from codecov_cli.runners.pytest_standard_runner import PytestStandardRunner
from tests.factory import FakeRunner


class TestRunners(object):
    # TODO: Extend with other standard runners once we create them (e.g. JS)

    @patch("codecov_cli.runners._load_runner_from_yaml")
    def test_load_runner_from_yaml_class_not_found(self, mocker):
        import tests.factory as fake_module

        mocker.patch("codecov_cli.runners.import_module", return_value=fake_module)

        with pytest.raises(AttributeError):
            _load_runner_from_yaml(
                {
                    "module": "mymodule.runner",
                    "class": "WrongClassName",
                    "params": {"collect_tests_response": ["list", "of", "labels"]},
                },
                {},
            )

    def test_load_runner_from_yaml_fail_instantiate_class(self, mocker):
        fake_module = mocker.MagicMock(FakeRunner=FakeRunner)
        mocker.patch("codecov_cli.runners.import_module", return_value=fake_module)
        with pytest.raises(TypeError):
            _load_runner_from_yaml(
                {
                    "module": "mymodule.runner",
                    "class": "FakeRunner",
                    "params": {"wrong_params": ["list", "of", "labels"]},
                },
                {},
            )

    def test_get_runner_dynamic_loading_unable_to_load_module(self, mocker):
        cli_config = {
            "runners": {
                "faultymod": {
                    "module": "nonexistent.module",
                    "class": "NonexistentClass",
                }
            }
        }
        mocker.patch(
            "codecov_cli.runners.import_module", side_effect=ModuleNotFoundError
        )
        with pytest.raises(ModuleNotFoundError):
            get_runner(cli_config=cli_config, runner_name="faultymod")
