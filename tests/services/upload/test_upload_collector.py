from pathlib import Path
from unittest.mock import patch

from codecov_cli.helpers.versioning_systems import GitVersioningSystem
from codecov_cli.services.upload.file_finder import FileFinder
from codecov_cli.services.upload.network_finder import NetworkFinder
from codecov_cli.services.upload.upload_collector import UploadCollector
from codecov_cli.types import UploadCollectionResultFile






@patch("codecov_cli.services.upload.upload_collector.open")






def test_fix_when_disabled_fixes(tmp_path):
    cpp_file = Path("tests/data/files_to_fix_examples/sample.cpp")

    col = UploadCollector(None, None, None, True)

    fixes = col._produce_file_fixes([cpp_file])

    assert len(fixes) == 0
    assert fixes == []


def test_generate_upload_data(tmp_path):
    (tmp_path / "sub").mkdir()
    (tmp_path / "sub" / "subsub").mkdir()
    (tmp_path / "node_modules").mkdir()

    should_find = [
        "abc-coverage.cov",
        "coverage-abc.abc",
        "sub/coverage-abc.abc",
        "sub/subsub/coverage-abc.abc",
        "coverage.abc",
        "jacocoxyz.xml",
        "sub/jacocoxyz.xml",
        "codecov.abc",
        "sub/subsub/codecov.abc",
        "xyz.codecov.abc",
        "sub/xyz.codecov.abc",
        "sub/subsub/xyz.codecov.abc",
        "cover.out",
        "abc.gcov",
        "sub/abc.gcov",
        "sub/subsub/abc.gcov",
    ]

    should_ignore = [
        "abc.codecov.exe",
        "sub/abc.codecov.exe",
        "codecov.exe",
        "__pycache__",
        "sub/subsub/__pycache__",
        ".gitignore",
        "a.sql",
        "a.csv",
        ".abc-coveragerc",
        ".coverage-xyz",
        "sub/scoverage.measurements.xyz",
        "sub/test_abcd_coverage.txt",
        "test-result-ff-codecoverage.json",
        "node_modules/abc-coverage.cov",
    ]

    for filename in should_find:
        (tmp_path / filename).touch()

    for filename in should_ignore:
        (tmp_path / filename).touch()

    file_finder = FileFinder(tmp_path)

    network_finder = NetworkFinder(GitVersioningSystem(), None, None, None)

    collector = UploadCollector([], network_finder, file_finder)

    res = collector.generate_upload_data()

    expected = {UploadCollectionResultFile(tmp_path / file) for file in should_find}

    for file in expected:
        assert file in res.files
