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
        "build_number,expected",
        [
            ("1234", "1234"),
            (None, None),
        ],
    )
    def test_build_code(self, build_number, expected, mocker):
        if build_number:
            mocker.patch.dict(os.environ, {"BITBUCKET_BUILD_NUMBER": build_number})
        else:
            mocker.patch.dict(os.environ, {}, clear=True)
        assert BitbucketAdapter()._get_build_code() == expected

    @pytest.mark.parametrize(
        "build_number,expected",
        [
            ("1234", "1234"),
            (None, None),
        ],
    )
    def test_job_code(self, build_number, expected, mocker):
        if build_number:
            mocker.patch.dict(os.environ, {"BITBUCKET_BUILD_NUMBER": build_number})
        else:
            mocker.patch.dict(os.environ, {}, clear=True)
        assert BitbucketAdapter()._get_job_code() == expected

    @pytest.mark.parametrize(
        "repo_full_name,expected",
        [
            ("org/repo", "org/repo"),
            (None, None),
        ],
    )
    def test_slug(self, repo_full_name, expected, mocker):
        if repo_full_name:
            mocker.patch.dict(os.environ, {"BITBUCKET_REPO_FULL_NAME": repo_full_name})
        else:
            mocker.patch.dict(os.environ, {}, clear=True)
        assert BitbucketAdapter()._get_slug() == expected
