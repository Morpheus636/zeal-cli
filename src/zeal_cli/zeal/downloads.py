import logging
import os
from pathlib import Path
import tarfile
import tempfile
from typing import Optional
import zipfile
import xml.etree.ElementTree as ET

import requests

from .config import config


logger = logging.getLogger(__name__)


def download_and_extract(url: str, extract_to: Path) -> None:
    """Downloads a zip file from a specified URL and extracts it to a specified location on disk.

    :param url: The URL to a .zip file to download and extract, in a string.
    :param extract_to: The path to a directory to extract the zip file to, in a string.
    :return: None
    """
    print(f"Downloading {url}")
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

def _write_xml(name: str, data:dict, output_location: Path):
    # create the root element
    root = ET.Element("entry")

    # create the version element and add it to the root
    version_elem = ET.SubElement(root, "version")
    version_elem.text = data["version"]

    # create the url elements and add them to the root
    for location in ["sanfrancisco", "london", "newyork", "tokyo", "frankfurt"]:
        url_elem = ET.SubElement(root, "url")
        url_elem.text = f"http://{location}.kapeli.com/feeds/zzz/user_contributed/build/{name}/{data['archive']}"

    # create the other-versions element and add it to the root
    other_versions_elem = ET.SubElement(root, "other-versions")

    if "specific_versions" in data:
        # create the version elements for the other versions and add them to the other-versions element
        for specific_version in data["specific_versions"]:
            if "version" in specific_version:
                version_elem = ET.SubElement(other_versions_elem, "version")
                name_elem = ET.SubElement(version_elem, "name")
                name_elem.text = specific_version["version"]

    # write the XML to a file
    tree = ET.ElementTree(root)
    feed_path = Path(output_location, f"{data['name'].replace('/', '_')}.xml").expanduser()
    feed_path.parent.mkdir(exist_ok=True,parents=False)
    tree.write(str(feed_path))

def _create_user_contributions_feeds(output_location: Path):
    resp = requests.get("https://kapeli.com/feeds/zzz/user_contributed/build/index.json")
    resp.raise_for_status()

    for name, definition in resp.json()["docsets"].items():
        _write_xml(name=name,data=definition,output_location=output_location)

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

    _create_user_contributions_feeds(output_location=Path(output_location, "user-contributed"))

    return output_location