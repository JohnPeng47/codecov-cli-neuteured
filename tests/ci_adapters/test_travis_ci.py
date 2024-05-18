import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.travis_ci import TravisCIAdapter


class TravisEnvEnum(str, Enum):
    TRAVIS_COMMIT = "TRAVIS_COMMIT"
    TRAVIS_BUILD_WEB_URL = "TRAVIS_BUILD_WEB_URL"
    TRAVIS_BUILD_NUMBER = "TRAVIS_BUILD_NUMBER"
    TRAVIS_JOB_NUMBER = "TRAVIS_JOB_NUMBER"
    TRAVIS_PULL_REQUEST = "TRAVIS_PULL_REQUEST"
    TRAVIS_REPO_SLUG = "TRAVIS_REPO_SLUG"
    TRAVIS_BRANCH = "TRAVIS_BRANCH"
    TRAVIS_PULL_REQUEST_SHA = "TRAVIS_PULL_REQUEST_SHA"
    TRAVIS_PULL_REQUEST_BRANCH = "TRAVIS_PULL_REQUEST_BRANCH"
    TRAVIS_JOB_ID = "TRAVIS_JOB_ID"
    CI = "CI"
    TRAVIS = "TRAVIS"
    SHIPPABLE = "SHIPPABLE"


class TestTravisCIAdapter(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            (
                {
                    TravisEnvEnum.TRAVIS_BRANCH: "abc",
                    TravisEnvEnum.TRAVIS_PULL_REQUEST_BRANCH: "pr-branch",
                },
                "pr-branch",
            ),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = TravisCIAdapter().get_fallback_value(FallbackFieldEnum.branch)

        assert actual == expected

    def test_service(self):
        assert (
            TravisCIAdapter().get_fallback_value(FallbackFieldEnum.service) == "travis"
        )
