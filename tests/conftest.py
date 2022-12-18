import pytest
import platform
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="session", autouse=True)
def mock_winreg():
    if platform.system() == "Windows":
        with patch("src.zeal.config.winreg") as patched_obj:
            patched_obj.OpenKey.return_value = MagicMock()
            patched_obj.QueryValueEx.return_value = ("C:/Users/unittestuser/AppData/Local/Zeal/Zealdupa/docsets", None)
            yield
    else:
        yield