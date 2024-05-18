import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.cirrus_ci import CirrusCIAdapter


class CirrusEnvEnum(str, Enum):
    CIRRUS_BRANCH = "CIRRUS_BRANCH"
    CIRRUS_BUILD_ID = "CIRRUS_BUILD_ID"
    CIRRUS_CHANGE_IN_REPO = "CIRRUS_CHANGE_IN_REPO"
    CIRRUS_REPO_FULL_NAME = "CIRRUS_REPO_FULL_NAME"
    CIRRUS_PR = "CIRRUS_PR"
    CIRRUS_TASK_ID = "CIRRUS_TASK_ID"
    CIRRUS_CI = "CIRRUS_CI"


class TestCirrus(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({CirrusEnvEnum.CIRRUS_BRANCH: "branch"}, "branch"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = CirrusCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            CirrusCIAdapter().get_fallback_value(FallbackFieldEnum.service) == "cirrus"
        )
