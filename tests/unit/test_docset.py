import os
import sys
import tempfile

import pytest


sys.path.append(os.path.relpath(__file__) + "/../src")
import src.zeal  # NOQA: E402


def test_list_all():
    with tempfile.TemporaryDirectory() as docset_dir:
        os.mkdir(os.path.join(docset_dir, "docset1.docset"))
        os.mkdir(os.path.join(docset_dir, "docset2.docset"))
        os.mkdir(os.path.join(docset_dir, "docset3.docset"))
        os.mkdir(os.path.join(docset_dir, "not_a_docset"))
        docset_list = src.zeal.docset.list_all(docset_dir=docset_dir)
        assert "docset1" in docset_list
        assert "docset2" in docset_list
        assert "docset3" in docset_list
        assert "not_a_docset" not in docset_list


def test_download_docset():
    with tempfile.TemporaryDirectory() as data_dir:
        # Setup the tempdir
        feeds_dir = os.path.join(data_dir, "feeds")
        os.mkdir(feeds_dir)
        docset_dir = os.path.join(data_dir, "docsets")
        os.mkdir(docset_dir)
        feeds_path = src.zeal.downloads.get_feeds(feeds_dir)
        # Test that the docset is downloaded to the right place
        src.zeal.docset.download("Django", feeds_path, docset_dir=docset_dir)
        assert os.path.isdir(os.path.join(docset_dir, "Django.docset"))
        with pytest.raises(src.zeal.exceptions.DocsetAlreadyInstalledError):
            src.zeal.docset.download("Django", feeds_path, docset_dir=docset_dir)


def test_delete_docset():
    with tempfile.TemporaryDirectory() as data_dir:
        # Setup the tempdir
        docset_dir = os.path.join(data_dir, "docsets")
        os.mkdir(docset_dir)
        # Test that the docset not existing raises an exception
        with pytest.raises(src.zeal.exceptions.DocsetNotInstalledError):
            src.zeal.docset.remove("TotallyRealDocset", docset_dir=docset_dir)
        # Test that a file with the same name still raises the exception
        with open(os.path.join(docset_dir, "TotallyRealDocset.docset"), "a"):
            pass
        with pytest.raises(src.zeal.exceptions.DocsetNotInstalledError):
            src.zeal.docset.remove("TotallyRealDocset", docset_dir=docset_dir)
        os.remove(os.path.join(docset_dir, "TotallyRealDocset.docset"))

        # Test that the docset gets removed when it exists.
        os.mkdir(os.path.join(docset_dir, "TotallyRealDocset.docset"))
        src.zeal.docset.remove("TotallyRealDocset", docset_dir=docset_dir)
        assert not os.path.isdir(os.path.join(docset_dir, "TotallyRealDocset.docset"))
