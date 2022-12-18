import sys
import os
from pathlib import Path
import pytest
import platform

sys.path.append(os.path.relpath(__file__) + "/../src")
import src.zeal  # NOQA: E402

@pytest.mark.skipif(platform.system() != "Windows", reason="Windows only test")
def test_config_is_mocked_properly():
    assert src.zeal.config.get_docset_dir() == Path("C:/Users/unittestuser/AppData/Local/Zeal/Zealdupa/docsets")