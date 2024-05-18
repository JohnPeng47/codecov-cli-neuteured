import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.droneci import DroneCIAdapter


class DroneCIEnvEnum(str, Enum):
    DRONE_BRANCH = "DRONE_BRANCH"
    DRONE_BUILD_NUMBER = "DRONE_BUILD_NUMBER"
    DRONE_BUILD_LINK = "DRONE_BUILD_LINK"
    DRONE_COMMIT_SHA = "DRONE_COMMIT_SHA"
    DRONE_REPO = "DRONE_REPO"
    DRONE_PULL_REQUEST = "DRONE_PULL_REQUEST"
    DRONE = "DRONE"


class TestDroneCI(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({DroneCIEnvEnum.DRONE_BRANCH: "random"}, "random"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = DroneCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            DroneCIAdapter().get_fallback_value(FallbackFieldEnum.service) == "droneci"
        )
