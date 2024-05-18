import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters import CircleCICIAdapter


class CircleCIEnvEnum(str, Enum):
    CIRCLE_SHA1 = "CIRCLE_SHA1"
    CIRCLE_BUILD_URL = "CIRCLE_BUILD_URL"
    CIRCLE_BUILD_NUM = "CIRCLE_BUILD_NUM"
    CIRCLE_NODE_INDEX = "CIRCLE_NODE_INDEX"
    CIRCLE_PR_NUMBER = "CIRCLE_PR_NUMBER"
    CIRCLE_PROJECT_USERNAME = "CIRCLE_PROJECT_USERNAME"
    CIRCLE_PROJECT_REPONAME = "CIRCLE_PROJECT_REPONAME"
    CIRCLE_REPOSITORY_URL = "CIRCLE_REPOSITORY_URL"
    CIRCLE_BRANCH = "CIRCLE_BRANCH"
    CI = "CI"
    CIRCLECI = "CIRCLECI"


class TestCircleCI(object):










    def test_raises_value_error_if_invalid_field(self):
        with pytest.raises(ValueError) as ex:
            CircleCICIAdapter().get_fallback_value("some random key x 123")

    def test_service(self):
        assert (
            CircleCICIAdapter().get_fallback_value(FallbackFieldEnum.service)
            == "circleci"
        )
