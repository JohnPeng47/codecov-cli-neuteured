import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.woodpeckerci import WoodpeckerCIAdapter


class WoodpeckerEnvEnum(str, Enum):
    CI_COMMIT_SOURCE_BRANCH = "CI_COMMIT_SOURCE_BRANCH"
    CI_COMMIT_BRANCH = "CI_COMMIT_BRANCH"
    CI_BUILD_NUMBER = "CI_BUILD_NUMBER"
    CI_BUILD_LINK = "CI_BUILD_LINK"
    CI_COMMIT_SHA = "CI_COMMIT_SHA"
    CI_REPO = "CI_REPO"
    CI_COMMIT_PULL_REQUEST = "CI_COMMIT_PULL_REQUEST"
    CI_JOB_NUMBER = "CI_JOB_NUMBER"
    CI = "CI"


class TestWoodpecker(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({WoodpeckerEnvEnum.CI_COMMIT_SOURCE_BRANCH: "aa"}, "aa"),
            ({WoodpeckerEnvEnum.CI_COMMIT_BRANCH: "bb"}, "bb"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        assert (
            WoodpeckerCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
            == expected
        )

    def test_service(self, mocker):
        assert (
            WoodpeckerCIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "woodpecker"
        )
