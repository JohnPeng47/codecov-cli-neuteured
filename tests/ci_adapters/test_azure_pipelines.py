import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters.azure_pipelines import AzurePipelinesCIAdapter


class AzurePipelinesEnvEnum(str, Enum):
    BUILD_BUILDID = "BUILD_BUILDID"
    BUILD_BUILDNUMBER = "BUILD_BUILDNUMBER"
    BUILD_SOURCEBRANCH = "BUILD_SOURCEBRANCH"
    BUILD_SOURCEVERSION = "BUILD_SOURCEVERSION"
    SYSTEM_PULLREQUEST_PULLREQUESTID = "SYSTEM_PULLREQUEST_PULLREQUESTID"
    SYSTEM_PULLREQUEST_PULLREQUESTNUMBER = "SYSTEM_PULLREQUEST_PULLREQUESTNUMBER"
    SYSTEM_TEAMFOUNDATIONCOLLECTIONURI = "SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"
    SYSTEM_TEAMPROJECT = "SYSTEM_TEAMPROJECT"
    BUILD_REPOSITORY_NAME = "BUILD_REPOSITORY_NAME"


class TestAzurePipelines(object):







    @pytest.mark.parametrize(
        "env_dict,expected",
        [
            ({}, None),
            ({AzurePipelinesEnvEnum.BUILD_SOURCEBRANCH: "refs/heads/main"}, "main"),
        ],
    )
    def test_branch(self, env_dict, expected, mocker):
        mocker.patch.dict(os.environ, env_dict)
        actual = AzurePipelinesCIAdapter().get_fallback_value(FallbackFieldEnum.branch)
        assert actual == expected

    def test_service(self):
        assert (
            AzurePipelinesCIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "azure_pipelines"
        )
