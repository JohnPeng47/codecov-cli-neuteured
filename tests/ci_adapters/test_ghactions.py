import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters import GithubActionsCIAdapter


class GithubActionsEnvEnum(str, Enum):
    GITHUB_SHA = "GITHUB_SHA"
    GITHUB_SERVER_URL = "GITHUB_SERVER_URL"
    GITHUB_RUN_ID = "GITHUB_RUN_ID"
    GITHUB_WORKFLOW = "GITHUB_WORKFLOW"
    GITHUB_HEAD_REF = "GITHUB_HEAD_REF"
    GITHUB_REF = "GITHUB_REF"
    GITHUB_REPOSITORY = "GITHUB_REPOSITORY"
    GITHUB_ACTIONS = "GITHUB_ACTIONS"


class TestGithubActions(object):









    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({GithubActionsEnvEnum.GITHUB_HEAD_REF: "random"}, "random"),
            ({GithubActionsEnvEnum.GITHUB_REF: r"doesn't_match"}, None),
            ({GithubActionsEnvEnum.GITHUB_REF: r"refs/heads/"}, None),
            ({GithubActionsEnvEnum.GITHUB_REF: r"refs/heads/abc"}, "abc"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict, clear=True)
        assert (
            GithubActionsCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
            == expected
        )

    def test_get_service(self, mocker):
        assert (
            GithubActionsCIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "github-actions"
        )
