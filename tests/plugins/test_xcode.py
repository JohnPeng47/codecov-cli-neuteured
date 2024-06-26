import pathlib
from functools import partial

import pytest

from codecov_cli.plugins.xcode import XcodePlugin
from tests.test_helpers import parse_outstreams_into_log_lines


class TestXcode(object):
    def act_like_xcrun_ran_succesfully(self, output_filename):
        # xcrun llvm-cov saves the output in a new created file
        # opening the file with write permission creates it if it does not exist
        result_file = open(output_filename, "w")
        result_file.close()

    def act_like_xcrun_is_not_installed(self, mocker):
        mocker.patch("codecov_cli.plugins.xcode.shutil.which", return_value=None)

    def act_like_xcrun_is_installed(self, mocker):
        mocker.patch("codecov_cli.plugins.xcode.shutil.which", return_value=True)






    def test_swift_cov_with_app_name_different_than_app_given_in_path(
        self, tmp_path, capsys, mocker
    ):
        dir_path = tmp_path / "Build/swift-example.app/swift-example"
        dir_path.parent.mkdir(parents=True, exist_ok=True)
        dir_path.touch()
        mocked_subprocess = mocker.patch(
            "codecov_cli.plugins.xcode.XcodePlugin.run_llvm_cov",
            side_effect=(
                lambda output_file_name, path, dest: partial(
                    self.act_like_xcrun_ran_succesfully, output_file_name
                )
            ),
        )
        XcodePlugin().swiftcov(dir_path, "different_app_name_than_swift-example")

        # assert run_llvm_cov is not called
        with pytest.raises(AssertionError):
            mocked_subprocess.assert_called_once()

    def test_run_llvm_cov(self, mocker):
        mocked_subprocess = mocker.patch(
            "codecov_cli.plugins.xcode.subprocess.run",
            return_value=mocker.MagicMock(returncode=0),
        )
        XcodePlugin().run_llvm_cov(
            output_file_name="llvm-output-test",
            path=mocker.MagicMock(),
            dest=mocker.MagicMock(),
        )
        mocked_subprocess.assert_called_once()
        file_path = pathlib.Path("llvm-output-test")
        assert file_path.is_file()
        file_path.unlink()
