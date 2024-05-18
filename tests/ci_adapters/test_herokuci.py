import os
from enum import Enum

import pytest

from codecov_cli.fallbacks import FallbackFieldEnum
from codecov_cli.helpers.ci_adapters import HerokuCIAdapter


class HerokuCIEnvEnum(str, Enum):
    HEROKU_TEST_RUN_BRANCH = "HEROKU_TEST_RUN_BRANCH"
    HEROKU_TEST_RUN_COMMIT_VERSION = "HEROKU_TEST_RUN_COMMIT_VERSION"
    HEROKU_TEST_RUN_ID = "HEROKU_TEST_RUN_ID"
    CI = "CI"


class TestHerokuCI(object):





    def test_service(self):
        assert (
            HerokuCIAdapter().get_fallback_value(FallbackFieldEnum.service) == "heroku"
        )

    def test_other_values_fallback_to_none(self):
        assert HerokuCIAdapter()._get_slug() == None
        assert HerokuCIAdapter()._get_build_url() == None
        assert HerokuCIAdapter()._get_job_code() == None
        assert HerokuCIAdapter()._get_pull_request_number() == None
