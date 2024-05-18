import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.teamcity import TeamcityAdapter


class TeamcityEnvEnum(str, Enum):
    BRANCH_NAME = "BRANCH_NAME"
    BUILD_NUMBER = "BUILD_NUMBER"
    BUILD_VCS_NUMBER = "BUILD_VCS_NUMBER"
    TEAMCITY_VERSION = "TEAMCITY_VERSION"


class TestBuildkite(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({TeamcityEnvEnum.BRANCH_NAME: "branch"}, "branch"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = TeamcityAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            TeamcityAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "teamcity"
        )
