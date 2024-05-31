import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.bitbucket_ci import BitbucketAdapter


class BitbucketEnvEnum(str, Enum):
    BITBUCKET_BUILD_NUMBER = "BITBUCKET_BUILD_NUMBER"
    BITBUCKET_BRANCH = "BITBUCKET_BRANCH"
    BITBUCKET_PR_ID = "BITBUCKET_PR_ID"
    BITBUCKET_COMMIT = "BITBUCKET_COMMIT"
    BITBUCKET_REPO_FULL_NAME = "BITBUCKET_REPO_FULL_NAME"
    CI = "CI"


class TestBitbucket(object):

    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({BitbucketEnvEnum.BITBUCKET_BRANCH: "abc"}, "abc"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = BitbucketAdapter().get_fallback_value(FallbackFieldEnum.branch)

        assert actual == expected

    def test_service(self):
        assert (
            BitbucketAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "bitbucket"
        )

    def test_service_name(self):
        assert BitbucketAdapter().get_service_name() == "Bitbucket"

    @pytest.mark.parametrize(
        "ci_env, build_number, expected_detect",
        [
            ({"CI": "true", "BITBUCKET_BUILD_NUMBER": "1234"}, "1234", True),
            ({"CI": "true"}, None, False),
            ({}, None, False),
        ],
    )
    def test_detect(self, ci_env, build_number, expected_detect, mocker):
        mocker.patch.dict(os.environ, ci_env)
        adapter = BitbucketAdapter()
        assert adapter.detect() == expected_detect
