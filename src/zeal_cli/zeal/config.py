import logging
import os
import platform
from typing import Any

if platform.system() == "Windows":
    import winreg

import yaml
from pathlib import Path


logger = logging.getLogger(__file__)


class Config:
    def _get_docset_dir(self) -> Path:
        # Set zeal_docset_dir variable.
        if platform.system() == "Linux":
            return Path("~", ".local", "share", "Zeal", "Zeal", "docsets").expanduser()
        elif platform.system() == "Windows":
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\\Zeal\\Zeal\\docsets") as key:
                path, _type = winreg.QueryValueEx(key, "path")
                return Path(path).expanduser()
        else:
            raise RuntimeError("Systems other than Linux and Windows are not supported")

    def _get_cli_data_dir(self) -> Path:
        zeal_cli_dir = Path("~", ".local", "share", "zeal_cli").expanduser()

        if zeal_cli_dir.is_file():
            logger.warning(
                f"The Zeal CLI data directory location ({zeal_cli_dir}) exists and is a file, not a directory. Deleting."
            )
            os.remove(zeal_cli_dir)
            zeal_cli_dir.mkdir(parents=True)
        elif zeal_cli_dir.is_dir():
            logger.debug(f"The Zeal CLI data directory location ({zeal_cli_dir}) already exists.")
        elif not zeal_cli_dir.exists():
            logger.debug(
                f"The Zeal CLI data directory location ({zeal_cli_dir}) does not exist. Creating."
            )
            zeal_cli_dir.mkdir(parents=True)
        return zeal_cli_dir

    def _set_default_config(self, config_path: Path) -> dict:
        config_dict = {"docset_dir": str(self._get_docset_dir().resolve())}
        if config_path.is_file():
            os.remove(config_path)
        with config_path.open(mode="x") as file:
            yaml.safe_dump(config_dict, stream=file)
        return config_dict

    def _get_config(self, config_path: Path) -> dict:
        if config_path.is_file():
            logger.debug(f"Using config file found at {config_path}.")
            with config_path.open() as file:
                config_dict = yaml.safe_load(file)
        else:
            logger.warning(f"Did not find a config file at {config_path}. Creating default.")
            config_dict = self._set_default_config(config_path)
        if not config_dict:
            logger.warning(f"Config file found at {config_path} is empty. Resetting to defaults.")
            config_dict = self._set_default_config(config_path)
        return config_dict

    def set_config_value(self, key: Any, value: Any, config_path: Path):
        with config_path.open(mode="r+") as config_file:
            config_dict = yaml.safe_load(config_file)
            config_dict[key] = value
            yaml.safe_dump(config_dict, stream=config_file)

    @property
    def cli_data_dir(self):
        return self._get_cli_data_dir()

    @property
    def cli_config_path(self):
        return Path(self.cli_data_dir, "config.yml")

    @property
    def cli_config(self):
        return self._get_config(self.cli_config_path)

    @property
    def docset_dir(self):
        if self.cli_config:
            return Path(self.cli_config["docset_dir"])


config = Config()
