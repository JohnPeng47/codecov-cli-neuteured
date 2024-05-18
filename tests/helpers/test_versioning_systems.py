from unittest.mock import MagicMock

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.versioning_systems import GitVersioningSystem


class TestGitVersioningSystem(object):



    def test_list_relevant_files_returns_correct_network_files(self, mocker, tmp_path):
        mocked_subprocess = MagicMock()
        mocker.patch(
            "codecov_cli.helpers.versioning_systems.subprocess.run",
            return_value=mocked_subprocess,
        )
        # git ls-files diplays a single \n as \\\\n
        mocked_subprocess.stdout = b'a.txt\nb.txt\n"a\\\\nb.txt"\nc.txt\nd.txt\n.circleci/config.yml\nLICENSE\napp/advanced calculations/advanced_calculator.js\n'

        vs = GitVersioningSystem()

        assert vs.list_relevant_files(tmp_path) == [
            "a.txt",
            "b.txt",
            "a\\nb.txt",
            "c.txt",
            "d.txt",
            ".circleci/config.yml",
            "LICENSE",
            "app/advanced calculations/advanced_calculator.js",
        ]

    def test_list_relevant_files_fails_if_no_root_is_found(self, mocker):
        mocker.patch(
            "codecov_cli.helpers.versioning_systems.GitVersioningSystem.get_network_root",
            return_value=None,
        )

        vs = GitVersioningSystem()
        with pytest.raises(ValueError) as ex:
            vs.list_relevant_files()
