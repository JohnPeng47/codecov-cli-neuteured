import re

import pytest

from codecov_cli.helpers.folder_searcher import globs_to_regex, search_files
















def test_globs_to_regex_returns_none_if_patterns_empty():
    regex = globs_to_regex([])

    assert regex is None


def test_search_directories(tmp_path):
    filename_include_regex = globs_to_regex(["*.app"])
    filepaths = [
        "banana.app/path/of/directory.txt",
        "path/to/apple.app/path/of/directorys",
        "path/to/banana.app/folder/test.txt",
        "apple.py",
        "banana.py",
    ]
    for f in filepaths:
        relevant_filepath = tmp_path / f
        relevant_filepath.parent.mkdir(parents=True, exist_ok=True)
        relevant_filepath.touch()
    expected_results = sorted(
        [
            tmp_path / "banana.app",
            tmp_path / "path/to/banana.app",
            tmp_path / "path/to/apple.app",
        ]
    )
    assert expected_results == sorted(
        search_files(
            tmp_path,
            [],
            filename_include_regex=filename_include_regex,
            filename_exclude_regex=None,
            search_for_directories=True,
        )
    )
