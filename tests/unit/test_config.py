import platform
from pathlib import Path

import pytest

import zeal_cli


@pytest.mark.skipif(platform.system() != "Windows", reason="Windows only test")
def test_config_is_mocked_properly():
    assert zeal_cli.zeal.config.config._get_docset_dir() == Path(
        "C:/Users/unittestuser/AppData/Local/Zeal/Zeal/docsets"
    )
