import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture(scope="session", autouse=True)
def mock_winreg():
    with patch("src.zeal.config.winreg") as patched_obj:
        key = MagicMock()
        patched_obj.OpenKey.return_value = key
        patched_obj.QueryValueEx.return_value = ("C:/Users/unittestuser/AppData/Local/Zeal/Zealdupa/docsets", None)
        yield