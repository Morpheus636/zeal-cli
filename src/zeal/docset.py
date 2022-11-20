import os
import platform
import shutil
import subprocess
import urllib
from pathlib import Path

import bs4

from . import config, downloads, exceptions

LATEST_VERSION = "latest"

def list_all(docset_dir: Path = config.docset_dir) -> list:
    """List the docsets in the docset_dir.

    :param docset_dir: String, path to the Zeal docset directory. DefaultL filesystem.docset_dir
    :return: List of docsets (by name, not by path)
    """
    installed_docsets = []
    for elem in docset_dir.glob("*.docset"):
        if elem.is_dir():
            installed_docsets.append(elem.stem)
    return installed_docsets


def download(docset_name: str, feeds_dir: Path, docset_version: str = LATEST_VERSION, docset_dir: Path = config.docset_dir) -> None:
    """Download a docset by its feed name.

    :param docset_name: String, the feed name of the docset to download
    :param feeds_dir: String, the feeds directory - use get_feeds() to create it and get its location.
    :param docset_version: String, the docset version to download. Default: zeal.docset.LATEST_VERSION
    :param docset_dir: String, the directory Zeal reads docsets from. Default: filesystem.docset_dir
    :return: None
    """
    # Raise an exception if the docset is already installed
    if docset_name in list_all(docset_dir=docset_dir):
        raise exceptions.DocsetAlreadyInstalledError(
            f"The docset '{docset_name}' is already installed."
        )

    # Get docset xml file
    docset_xml_path = _get_docset_xml(docset_name, feeds_dir)

    # Extract the URL and download it to the docset dir
    with docset_xml_path.open() as file:
        file_contents = file.read()
        soup = bs4.BeautifulSoup(file_contents, "lxml")
        urls = soup.find_all("url")
        url = urls[0].getText()
        # Adjust URL if version is specified
        if docset_version != LATEST_VERSION:
            # Verify if version is available in feed
            if soup.find("other-versions") and soup.findAll(string=docset_version):
                parsed_uri = urllib.parse.urlparse(url)
                file_name = os.path.basename(parsed_uri.path)
                url = f"{parsed_uri.scheme}://{parsed_uri.netloc}/feeds/zzz/versions/{docset_name}/{docset_version}/{file_name}"
            else:
                raise exceptions.DocsetNotExistsError(
                    f"Version {docset_version} does not exist for {docset_name}"
                )

    downloads.download_and_extract(url, docset_dir)


def remove(docset_name: str, docset_dir: Path = config.docset_dir):
    """

    :param docset_name: String, the name of the docset to remove
    :param docset_dir: Optional: String, the path to the docset directory. Default: filesystem.docset_dir
    :return:
    """
    if docset_name not in list_all(docset_dir=docset_dir):
        raise exceptions.DocsetNotInstalledError(
            f"The docset to remove '{docset_name}' cannot be removed because it is not installed on your system."
        )
    if platform.system() == "Windows":
        # windows performance of shutil.rmtree is pathetic
        subprocess.run(["rmdir", "/q", "/s", str(Path(docset_dir, f"{docset_name}.docset").resolve())], check=True, shell=True)
    else:
        shutil.rmtree(str(Path(docset_dir, f"{docset_name}.docset").resolve()))

def get_docset_versions(docset_name: str, feeds_dir: Path):
    """Returns a list of available versions of a particular docset.

    :param docset_name: String, the name of the docset to remove
    :param feeds_dir: String, the feeds directory - use get_feeds() to create it and get its location.
    :return: List of version as string
    """
    docset_xml_path = _get_docset_xml(docset_name, feeds_dir)

    # Extract the URL and download it to the docset dir
    with open(docset_xml_path, "r") as file:
        file_contents = file.read()
        soup = bs4.BeautifulSoup(file_contents, "lxml")
        # Verify if version is available in feed
        if soup.find("other-versions"):
            soup_docset_versions = soup.findAll('version')
            return [docset_version.get_text() for docset_version in soup_docset_versions]


def _get_docset_xml(docset_name: str, feeds_dir: Path) -> Path:
    """Returns the correct docset xml file

    :param docset_name: String, the name of the docset to remove
    :param feeds_dir: String, the feeds directory - use get_feeds() to create it and get its location.
    :return: the docset xml file path
    """
    for elem in feeds_dir.glob("*.xml"):
        if elem.stem == docset_name:
            return elem
    raise exceptions.DocsetNotExistsError(
            f"The docset '{docset_name}' cannot be found in the feeds to download."
    )