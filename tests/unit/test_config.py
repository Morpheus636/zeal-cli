import sys
import os
from pathlib import Path
import pytest

sys.path.append(os.path.relpath(__file__) + "/../src")
import src.zeal  # NOQA: E402

def test_config_is_mocked_properly():
    assert src.zeal.config.get_docset_dir() == Path("C:/Users/unittestuser/AppData/Local/Zeal/Zealdupa/docsets")