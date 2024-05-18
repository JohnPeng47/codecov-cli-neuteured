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
