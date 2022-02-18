import os
import sys
import tempfile


sys.path.append(os.path.relpath(__file__) + "/../src")
import src.zeal  # NOQA: E402


def test_get_feeds():
    with tempfile.TemporaryDirectory() as data_dir:
        feeds_path = src.zeal.download_docset.get_feeds(data_dir=data_dir)
        assert os.path.isdir(feeds_path)
        assert os.path.isfile(os.path.join(feeds_path, "Django.xml"))
        assert os.path.isfile(os.path.join(feeds_path, "Python_3.xml"))


def test_download_docset():
    with tempfile.TemporaryDirectory() as data_dir:
        feeds_dir = os.path.join(data_dir, "feeds")
        os.mkdir(feeds_dir)
        docset_dir = os.path.join(data_dir, "docsets")
        os.mkdir(docset_dir)
        feeds_path = src.zeal.download_docset.get_feeds(feeds_dir)
        src.zeal.download_docset.download_docset("Django", feeds_path, docset_dir=docset_dir)
        assert os.path.isdir(os.path.join(docset_dir, "Django.docset"))
