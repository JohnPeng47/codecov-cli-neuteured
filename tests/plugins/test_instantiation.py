from codecov_cli.plugins import (
    GcovPlugin,
    NoopPlugin,
    XcodePlugin,
    _get_plugin,
    _load_plugin_from_yaml,
    select_preparation_plugins,
)
from codecov_cli.plugins.compress_pycoverage_contexts import CompressPycoverageContexts
from codecov_cli.plugins.pycoverage import Pycoverage, PycoverageConfig






















def test_get_plugin_compress_pycoverage():
    res = _get_plugin({}, "compress-pycoverage")
    assert isinstance(res, CompressPycoverageContexts)

    res = _get_plugin(
        {"plugins": {"compress-pycoverage": {"file_to_compress": "something.json"}}},
        "compress-pycoverage",
    )
    assert isinstance(res, CompressPycoverageContexts)
    assert str(res.file_to_compress) == "something.json"


def test_select_preparation_plugins(mocker):
    class SamplePlugin(object):
        def __init__(self, banana=None):
            pass

    SampleModule = mocker.MagicMock(SamplePlugin=SamplePlugin)

    class SecondSamplePlugin(object):
        def __init__(self, banana=None):
            pass

    SecondSampleModule = mocker.MagicMock(SecondSamplePlugin=SecondSamplePlugin)

    mocker.patch(
        "codecov_cli.plugins.import_module",
        side_effect=[ModuleNotFoundError, SampleModule, SecondSampleModule],
    )

    res = select_preparation_plugins(
        {
            "plugins": {
                "otherthing": {
                    "module": "a",
                    "class": "SamplePlugin",
                    "params": {"banana": "apple", "pineapple": 2},
                },
                "second": {
                    "module": "c",
                    "class": "SecondSamplePlugin",
                    "params": {"banana": "apple"},
                },
                "something": {"module": "e", "class": "f"},
            }
        },
        ["gcov", "something", "otherthing", "second", "lalalala"],
    )
    assert len(res) == 5
    assert isinstance(res[0], GcovPlugin)
    assert isinstance(res[1], NoopPlugin)
    assert isinstance(res[2], NoopPlugin)
    assert isinstance(res[3], SecondSamplePlugin)
    assert isinstance(res[4], NoopPlugin)
