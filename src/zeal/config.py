import logging
import os
import platform

import yaml


logger = logging.getLogger(__file__)


def get_docset_dir() -> str:
    # Set zeal_docset_dir variable.
    if platform.system() == "Linux":
        return os.path.join(os.path.expanduser("~"), ".local", "share", "Zeal", "Zeal", "docsets")
    else:
        raise NotImplementedError("Zeal_CLI only supports linux at this time.")


def get_cli_data_dir() -> str:
    if platform.system() == "Linux":
        zeal_cli_dir = os.path.join(os.path.expanduser("~"), ".local", "share", "zeal_cli")
    else:
        raise NotImplementedError("Zeal_CLI only supports linux at this time.")

    if os.path.isfile(zeal_cli_dir):
        logger.warning(
            f"The Zeal CLI data directory location ({zeal_cli_dir}) exists and is a file, not a directory. Deleting."
        )
        os.remove(zeal_cli_dir)
        os.makedirs(zeal_cli_dir)
    elif os.path.isdir(zeal_cli_dir):
        logger.debug(f"The Zeal CLI data directory location ({zeal_cli_dir}) already exists.")
    elif not os.path.exists(zeal_cli_dir):
        logger.debug(
            f"The Zeal CLI data directory location ({zeal_cli_dir}) does not exist. Creating."
        )
        os.makedirs(zeal_cli_dir)
    return zeal_cli_dir


def set_default_config(config_path: str) -> dict:
    config_dict = {"docset_dir": get_docset_dir()}
    with open(config_path, "x") as file:
        yaml.safe_dump(config_dict, stream=file)
    return config_dict


def get_config(data_dir: str) -> dict:
    config_path = os.path.join(data_dir, "config.yml")
    if os.path.isfile(config_path):
        logger.debug(f"Using config file found at {config_path}.")
        with open(config_path, "r") as file:
            config_dict = yaml.safe_load(file)
    else:
        logger.warning(f"Did not find a config file at {config_path}. Creating default.")
        config_dict = set_default_config(config_path)
    return config_dict


cli_data_dir = get_cli_data_dir()
config = get_config(cli_data_dir)
docset_dir = config["docset_dir"]
