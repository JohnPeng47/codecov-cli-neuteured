import os

from codecov_cli.helpers.ci_adapters import (
    AppveyorCIAdapter,
    AWSCodeBuildCIAdapter,
    AzurePipelinesCIAdapter,
    BitbucketAdapter,
    BitriseCIAdapter,
    BuildkiteAdapter,
    CircleCICIAdapter,
    CirrusCIAdapter,
    DroneCIAdapter,
    GithubActionsCIAdapter,
    GitlabCIAdapter,
    HerokuCIAdapter,
    JenkinsAdapter,
    LocalAdapter,
    TeamcityAdapter,
    TravisCIAdapter,
    WoodpeckerCIAdapter,
    get_ci_adapter,
)


class TestCISelector(object):


















    def test_auto_return_gh_actions(self, mocker):
        mocker.patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}, clear=True)
        assert isinstance(get_ci_adapter(), GithubActionsCIAdapter)

    def test_auto_return_circle_ci(self, mocker):
        mocker.patch.dict(os.environ, {"CIRCLECI": "true", "CI": "true"}, clear=True)
        assert isinstance(get_ci_adapter(), CircleCICIAdapter)
