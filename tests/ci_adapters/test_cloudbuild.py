import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.cloudbuild import GoogleCloudBuildAdapter


class CloudBuildEnvEnum(str, Enum):
    BRANCH_NAME = "BRANCH_NAME"
    BUILD_ID = "BUILD_ID"
    COMMIT_SHA = "COMMIT_SHA"
    LOCATION = "LOCATION"
    PROJECT_ID = "PROJECT_ID"
    PROJECT_NUMBER = "PROJECT_NUMBER"
    REPO_FULL_NAME = "REPO_FULL_NAME"
    _PR_NUMBER = "_PR_NUMBER"
    TRIGGER_NAME = "TRIGGER_NAME"


class TestCloudBuild(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({CloudBuildEnvEnum.REPO_FULL_NAME: "owner/repo"}, "owner/repo"),
        ],
    )
    def test_slug(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = GoogleCloudBuildAdapter().get_fallback_value(FallbackFieldEnum.slug)

        assert actual == expected

    def test_service(self):
        assert (
            GoogleCloudBuildAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "google_cloud_build"
        )
