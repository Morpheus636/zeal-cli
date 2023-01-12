import pytest
import platform
from pathlib import Path
from unittest.mock import patch


@pytest.fixture(scope="session", autouse=True)
def mock_winreg():
    if platform.system() == "Windows":
        with patch("src.zeal_cli.zeal.config.config") as patched_obj:
            patched_obj._get_docset_dir.return_value = Path(
                "C:/Users/unittestuser/AppData/Local/Zeal/Zeal/docsets"
            )
            yield
    else:
        yield
