import os
import sys
import tempfile


sys.path.append(os.path.relpath(__file__) + "/../src")
import src.zeal  # NOQA: E402


def test_get_feeds():
    with tempfile.TemporaryDirectory() as data_dir:
        feeds_path = src.zeal.downloads.get_feeds(data_dir=data_dir)
        assert os.path.isdir(feeds_path)
        assert os.path.isfile(os.path.join(feeds_path, "Django.xml"))
        assert os.path.isfile(os.path.join(feeds_path, "Python_3.xml"))
