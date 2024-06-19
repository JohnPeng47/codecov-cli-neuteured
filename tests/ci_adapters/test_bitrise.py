import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.bitrise_ci import BitriseCIAdapter


class BitriseEnvEnum(str, Enum):
    BITRISE_GIT_BRANCH = "BITRISE_GIT_BRANCH"
    BITRISE_PULL_REQUEST = "BITRISE_PULL_REQUEST"
    BITRISE_BUILD_NUMBER = "BITRISE_BUILD_NUMBER"
    BITRISE_BUILD_URL = "BITRISE_BUILD_URL"
    GIT_CLONE_COMMIT_HASH = "GIT_CLONE_COMMIT_HASH"
    CI = "CI"
    BITRISE_IO = "BITRISE_IO"


class TestBitrise(object):

    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({BitriseEnvEnum.BITRISE_GIT_BRANCH: "branch"}, "branch"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = BitriseCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            BitriseCIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "bitrise"
        )

    @pytest.mark.parametrize(
        "env_name,env_value,expected,method",
        [
            (
                "GIT_CLONE_COMMIT_HASH",
                "commitsha1234",
                "commitsha1234",
                "_get_commit_sha",
            ),
            (
                "BITRISE_BUILD_URL",
                "http://buildurl.com",
                "http://buildurl.com",
                "_get_build_url",
            ),
            ("BITRISE_BUILD_NUMBER", "42", "42", "_get_build_code"),
            ("BITRISE_PULL_REQUEST", "10", "10", "_get_pull_request_number"),
        ],
    )
    def test_private_methods(self, env_name, env_value, expected, method, mocker):
        mocker.patch.dict(os.environ, {env_name: env_value})
        bitrise_adapter = BitriseCIAdapter()
        actual = getattr(bitrise_adapter, method)()
        assert actual == expected
