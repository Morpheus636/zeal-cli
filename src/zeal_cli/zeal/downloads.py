import logging
import os
from pathlib import Path
import tarfile
import tempfile
from typing import Optional
import zipfile

import requests

from .config import config


logger = logging.getLogger(__name__)


def download_and_extract(url: str, extract_to: Path) -> None:
    """Downloads a zip file from a specified URL and extracts it to a specified location on disk.

    :param url: The URL to a .zip file to download and extract, in a string.
    :param extract_to: The path to a directory to extract the zip file to, in a string.
    :return: None
    """
    with tempfile.TemporaryDirectory() as tempdir:
        # Download Phase
        if url.endswith(".zip"):
            file_name = os.path.join(tempdir, "zipfile.zip")
        elif url.endswith(".tgz"):
            file_name = os.path.join(tempdir, "tarball.tgz")
        with requests.get(url, stream=True) as response:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(512):
                    file.write(chunk)

        # Extract Phase
        if url.endswith(".zip"):
            with zipfile.ZipFile(file_name, "r") as zip_ref:
                zip_ref.extractall(str(extract_to.resolve()))
        elif url.endswith(".tgz"):
            with tarfile.open(file_name, "r:gz") as tar_ref:
                tar_ref.extractall(str(extract_to.resolve()))


def get_feeds(data_dir: Optional[Path] = None) -> Path:
    """Downloads Dash's feeds repository to extract the mirror URLs from.

    :param data_dir: a pathlib.Path pointing to the zeal_cli data directory. Default: config.cli_data_dir
    :return: a pathlib.Path pointing to the feeds directory.
    """
    if data_dir is None:
        data_dir = config.cli_data_dir
    url = "https://github.com/Kapeli/feeds/archive/refs/heads/master.zip"
    output_location = Path(data_dir, "feeds")  # Figure out where to put the feeds dir
    download_and_extract(url, output_location)
    output_location = Path(output_location, "feeds-master")
    return output_location
