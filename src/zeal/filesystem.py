import logging
import os
import platform


logger = logging.getLogger(__file__)


def get_docset_dir():
    # Set zeal_docset_dir variable.
    if platform.system() == "Linux":
        return os.path.join(os.path.expanduser("~"), ".local", "share", "Zeal", "Zeal", "docsets")
    else:
        raise NotImplementedError("Zeal_CLI only supports linux at this time.")


def get_cli_data_dir():
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


cli_data_dir = get_cli_data_dir()
docset_dir = get_docset_dir()
