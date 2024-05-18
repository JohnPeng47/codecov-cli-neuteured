import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters import GitlabCIAdapter


class GitlabCIEnvEnum(str, Enum):
    CI_MERGE_REQUEST_SOURCE_BRANCH_SHA = "CI_MERGE_REQUEST_SOURCE_BRANCH_SHA"
    CI_BUILD_REF = "CI_BUILD_REF"
    CI_COMMIT_REF_NAME = "CI_COMMIT_REF_NAME"
    CI_BUILD_REF_NAME = "CI_BUILD_REF_NAME"
    CI_REPOSITORY_URL = "CI_REPOSITORY_URL"
    CI_BUILD_REPO = "CI_BUILD_REPO"
    CI_PROJECT_PATH = "CI_PROJECT_PATH"
    CI_JOB_ID = "CI_JOB_ID"
    CI_BUILD_ID = "CI_BUILD_ID"
    CI_JOB_URL = "CI_JOB_URL"
    CI_COMMIT_SHA = "CI_COMMIT_SHA"
    CI_MERGE_REQUEST_IID = "CI_MERGE_REQUEST_IID"
    CI_PROJECT_NAMESPACE = "CI_PROJECT_NAMESPACE"
    CI_PROJECT_NAME = "CI_PROJECT_NAME"
    GITLAB_CI = "GITLAB_CI"


class TestGitlabCI(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({GitlabCIEnvEnum.CI_COMMIT_REF_NAME: "aa"}, "aa"),
            ({GitlabCIEnvEnum.CI_BUILD_REF_NAME: "bb"}, "bb"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        assert (
            GitlabCIAdapter().get_fallback_value(FallbackFieldEnum.branch) == expected
        )

    def test_service(self, mocker):
        assert (
            GitlabCIAdapter().get_fallback_value(FallbackFieldEnum.service) == "gitlab"
        )
