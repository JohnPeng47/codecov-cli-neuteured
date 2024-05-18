import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.local import LocalAdapter


class LocalEnvEnum(str, Enum):
    GIT_BRANCH = "GIT_BRANCH"
    BRANCH_NAME = "BRANCH_NAME"
    GIT_COMMIT = "GIT_COMMIT"


class TestLocalAdapter(object):








    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({LocalEnvEnum.BRANCH_NAME: "branch"}, "branch"),
            ({LocalEnvEnum.GIT_BRANCH: "branch"}, "branch"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = LocalAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert LocalAdapter().get_fallback_value(FallbackFieldEnum.service) == "local"
