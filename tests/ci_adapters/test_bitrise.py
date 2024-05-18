import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.bitrise_ci import BitriseCIAdapter


class BitriseEnvEnum(str, Enum):
    BITRISE_GIT_BRANCH = "BITRISE_GIT_BRANCH"
    BITRISE_PULL_REQUEST = "BITRISE_PULL_REQUEST"
    BITRISE_BUILD_NUMBER = "BITRISE_BUILD_NUMBER"
    BITRISE_BUILD_URL = "BITRISE_BUILD_URL"
    GIT_CLONE_COMMIT_HASH = "GIT_CLONE_COMMIT_HASH"
    CI = "CI"
    BITRISE_IO = "BITRISE_IO"


class TestBitrise(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({BitriseEnvEnum.BITRISE_GIT_BRANCH: "branch"}, "branch"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = BitriseCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            BitriseCIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "bitrise"
        )
