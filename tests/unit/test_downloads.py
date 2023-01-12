import os
import tempfile

import zeal_cli


def test_get_feeds():
    with tempfile.TemporaryDirectory() as data_dir:
        feeds_path = zeal_cli.zeal.downloads.get_feeds(data_dir=data_dir)
        assert os.path.isdir(feeds_path)
        assert os.path.isfile(os.path.join(feeds_path, "Django.xml"))
        assert os.path.isfile(os.path.join(feeds_path, "Python_3.xml"))
