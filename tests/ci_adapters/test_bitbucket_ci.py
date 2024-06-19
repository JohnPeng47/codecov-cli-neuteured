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

    @pytest.mark.parametrize(
        "env_var,value,expected",
        [
            ("BITBUCKET_COMMIT", "1234567890abcdef", "1234567890abcdef"),
            ("BITBUCKET_COMMIT", "1234567890ab", None),
            ("BITBUCKET_COMMIT", None, None),
        ],
    )
    def test_get_commit_sha(self, env_var, value, expected, mocker):
        mocker.patch.dict(os.environ, {env_var: value} if value is not None else {})
        adapter = BitbucketAdapter()
        assert adapter._get_commit_sha() == expected
