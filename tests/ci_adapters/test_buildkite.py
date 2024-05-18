import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.buildkite import BuildkiteAdapter


class BuildkiteEnvEnum(str, Enum):
    BUILDKITE_BRANCH = "BUILDKITE_BRANCH"
    BUILDKITE_BUILD_NUMBER = "BUILDKITE_BUILD_NUMBER"
    BUILDKITE_BUILD_URL = "BUILDKITE_BUILD_URL"
    BUILDKITE_COMMIT = "BUILDKITE_COMMIT"
    BUILDKITE_ORGANIZATION_SLUG = "BUILDKITE_ORGANIZATION_SLUG"
    BUILDKITE_PIPELINE_SLUG = "BUILDKITE_PIPELINE_SLUG"
    BUILDKITE_PULL_REQUEST = "BUILDKITE_PULL_REQUEST"
    BUILDKITE_JOB_ID = "BUILDKITE_JOB_ID"
    BUILDKITE = "BUILDKITE"


class TestBuildkite(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({BuildkiteEnvEnum.BUILDKITE_BRANCH: "branch"}, "branch"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = BuildkiteAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            BuildkiteAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "buildkite"
        )
