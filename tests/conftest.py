import pytest
import platform
from pathlib import Path
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="session", autouse=True)
def mock_winreg():
    if platform.system() == "Windows":
        with patch("src.zeal.config") as patched_obj:
            patched_obj.get_docset_dir.return_value = Path("C:/Users/unittestuser/AppData/Local/Zeal/Zeal/docsets")
            yield
    else:
        yield
