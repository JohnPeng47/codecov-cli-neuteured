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

    def test_get_service_name(self):
        adapter = BitriseCIAdapter()
        assert adapter.get_service_name() == "Bitrise"

    def test_job_code_none(self):
        adapter = BitriseCIAdapter()
        assert adapter._get_job_code() is None

    @pytest.mark.parametrize(
        "env_var, expected",
        [
            ({"CI": "true", "BITRISE_IO": "true"}, True),
            ({"CI": "true", "BITRISE_IO": ""}, False),
            ({"CI": "", "BITRISE_IO": "true"}, False),
            ({"CI": "", "BITRISE_IO": ""}, False),
        ],
    )
    def test_detect(self, env_var, expected, mocker):
        mocker.patch.dict(os.environ, env_var)
        adapter = BitriseCIAdapter()
        assert adapter.detect() == expected

    @pytest.mark.parametrize(
        "env_var,expected",
        [
            ({"BITRISE_PULL_REQUEST": "42"}, "42"),
            ({}, None),
        ],
    )
    def test_pull_request_number(self, env_var, expected, mocker):
        mocker.patch.dict(os.environ, env_var)
        adapter = BitriseCIAdapter()
        assert adapter._get_pull_request_number() == expected

    @pytest.mark.parametrize(
        "env_var, expected",
        [
            ({"BITRISE_BUILD_NUMBER": "1234"}, "1234"),
            ({}, None),
        ],
    )
    def test_get_build_code(self, env_var, expected, mocker):
        mocker.patch.dict(os.environ, env_var)
        adapter = BitriseCIAdapter()
        assert adapter._get_build_code() == expected
