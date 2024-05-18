from codecov_cli.types import UploadCollectionResultFile


class TestUploadCollectionResultFile(object):

    def test_get_content(self, tmp_path):
        content = b"first line\nsecondline\nlastline\n"
        sub = tmp_path / "sub"
        sub.mkdir()
        file = sub / "a.txt"
        file.write_bytes(content)

        assert UploadCollectionResultFile(file).get_content() == content

    def test_eq(self, tmp_path):
        p = tmp_path / "a.txt"

        assert object() != UploadCollectionResultFile(p)

        assert UploadCollectionResultFile(p) == UploadCollectionResultFile(p)
