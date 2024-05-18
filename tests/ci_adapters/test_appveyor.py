import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.appveyor_ci import AppveyorCIAdapter


class AppveyorCIEnvEnum(str, Enum):
    APPVEYOR_ACCOUNT_NAME = "APPVEYOR_ACCOUNT_NAME"
    APPVEYOR_BUILD_ID = "APPVEYOR_BUILD_ID"
    APPVEYOR_BUILD_VERSION = "APPVEYOR_BUILD_VERSION"
    APPVEYOR_JOB_ID = "APPVEYOR_JOB_ID"
    APPVEYOR_PROJECT_SLUG = "APPVEYOR_PROJECT_SLUG"
    APPVEYOR_PULL_REQUEST_HEAD_COMMIT = "APPVEYOR_PULL_REQUEST_HEAD_COMMIT"
    APPVEYOR_PULL_REQUEST_NUMBER = "APPVEYOR_PULL_REQUEST_NUMBER"
    APPVEYOR_REPO_BRANCH = "APPVEYOR_REPO_BRANCH"
    APPVEYOR_REPO_COMMIT = "APPVEYOR_REPO_COMMIT"
    APPVEYOR_REPO_NAME = "APPVEYOR_REPO_NAME"
    APPVEYOR_URL = "APPVEYOR_URL"
    CI = "CI"
    APPVEYOR = "APPVEYOR"


class TestAppveyorCI(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({AppveyorCIEnvEnum.APPVEYOR_REPO_BRANCH: "abc"}, "abc"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = AppveyorCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            AppveyorCIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "appveyor"
        )
