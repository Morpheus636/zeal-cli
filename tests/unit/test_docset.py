import os
import tempfile
from pathlib import Path

import pytest

import zeal_cli


@pytest.fixture(scope="class")
def setup_temporary_dir():
    with tempfile.TemporaryDirectory() as data_dir:
        # Setup the tempdir
        feeds_dir = os.path.join(data_dir, "feeds")
        os.mkdir(feeds_dir)
        docset_dir = os.path.join(data_dir, "docsets")
        os.mkdir(docset_dir)
        feeds_path = zeal_cli.zeal.downloads.get_feeds(feeds_dir)
        yield (feeds_dir, docset_dir, feeds_path)


class TestBasic:
    def test_list_all(
        self,
    ):
        with tempfile.TemporaryDirectory() as docset_dir:
            os.mkdir(os.path.join(docset_dir, "docset1.docset"))
            os.mkdir(os.path.join(docset_dir, "docset2.docset"))
            os.mkdir(os.path.join(docset_dir, "docset3.docset"))
            os.mkdir(os.path.join(docset_dir, "not_a_docset"))
            docset_list = zeal_cli.zeal.docset.list_all(docset_dir=Path(docset_dir))
            assert "docset1" in docset_list
            assert "docset2" in docset_list
            assert "docset3" in docset_list
            assert "not_a_docset" not in docset_list

    def test_download_docset(self, setup_temporary_dir):
        _, docset_dir, feeds_path = setup_temporary_dir

        # Test that the docset is downloaded to the right place
        zeal_cli.zeal.docset.download("Django", feeds_path, docset_dir=Path(docset_dir))
        assert os.path.isdir(os.path.join(docset_dir, "Django.docset"))
        with pytest.raises(zeal_cli.zeal.exceptions.DocsetAlreadyInstalledError):
            zeal_cli.zeal.docset.download("Django", feeds_path, docset_dir=Path(docset_dir))

    def test_delete_docset(self, setup_temporary_dir):
        _, docset_dir, feeds_path = setup_temporary_dir

        # Test that the docset not existing raises an exception
        with pytest.raises(zeal_cli.zeal.exceptions.DocsetNotInstalledError):
            zeal_cli.zeal.docset.remove("TotallyRealDocset", docset_dir=Path(docset_dir))
        # Test that a file with the same name still raises the exception
        with open(os.path.join(docset_dir, "TotallyRealDocset.docset"), "a"):
            pass
        with pytest.raises(zeal_cli.zeal.exceptions.DocsetNotInstalledError):
            zeal_cli.zeal.docset.remove("TotallyRealDocset", docset_dir=Path(docset_dir))
        os.remove(os.path.join(docset_dir, "TotallyRealDocset.docset"))

        # Test that the docset gets removed when it exists.
        os.mkdir(os.path.join(docset_dir, "TotallyRealDocset.docset"))
        zeal_cli.zeal.docset.remove("TotallyRealDocset", docset_dir=Path(docset_dir))
        assert not os.path.isdir(os.path.join(docset_dir, "TotallyRealDocset.docset"))

    def test_list_docset_version(self, setup_temporary_dir):
        _, docset_dir, feeds_path = setup_temporary_dir

        # Test that for a docset a list of version strings is returned
        docset_versions = zeal_cli.zeal.docset.get_docset_versions("Django", feeds_path)
        assert isinstance(docset_versions, list)
        assert all(isinstance(version, str) for version in docset_versions)


class TestDoubleDownload:
    def test_download_docset_by_version(self, setup_temporary_dir):
        _, docset_dir, feeds_path = setup_temporary_dir

        # Test that the docset is downloaded to the right place
        zeal_cli.zeal.docset.download(
            "Django", feeds_path, docset_version="2.2.7", docset_dir=Path(docset_dir)
        )
        assert os.path.isdir(os.path.join(docset_dir, "Django.docset"))
        with pytest.raises(zeal_cli.zeal.exceptions.DocsetAlreadyInstalledError):
            zeal_cli.zeal.docset.download(
                "Django", feeds_path, docset_version="2.2.7", docset_dir=Path(docset_dir)
            )
