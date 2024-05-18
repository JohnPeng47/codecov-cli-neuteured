import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.codebuild import AWSCodeBuildCIAdapter


class CodeBuildEnvEnum(str, Enum):
    CODEBUILD_WEBHOOK_HEAD_REF = "CODEBUILD_WEBHOOK_HEAD_REF"
    CODEBUILD_BUILD_ID = "CODEBUILD_BUILD_ID"
    CODEBUILD_RESOLVED_SOURCE_VERSION = "CODEBUILD_RESOLVED_SOURCE_VERSION"
    CODEBUILD_SOURCE_REPO_URL = "CODEBUILD_SOURCE_REPO_URL"
    CODEBUILD_SOURCE_VERSION = "CODEBUILD_SOURCE_VERSION"
    CODEBUILD_CI = "CODEBUILD_CI"


class TestCodeBuild(object):






    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            (
                {CodeBuildEnvEnum.CODEBUILD_WEBHOOK_HEAD_REF: "refs/heads/branch"},
                "branch",
            ),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = AWSCodeBuildCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            AWSCodeBuildCIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "AWS CodeBuild"
        )
