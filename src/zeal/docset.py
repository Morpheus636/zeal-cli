import os
import shutil
import urllib

import bs4

from . import config, downloads, exceptions


def list_all(docset_dir: str = config.docset_dir) -> list:
    """List the docsets in the docset_dir.

    :param docset_dir: String, path to the Zeal docset directory. DefaultL filesystem.docset_dir
    :return: List of docsets (by name, not by path)
    """
    files_list = os.listdir(docset_dir)
    installed_docsets = []
    for file in files_list:
        if os.path.isdir(os.path.join(docset_dir, file)) and file.endswith(".docset"):
            installed_docsets.append(file.removesuffix(".docset"))
    return installed_docsets


def download(docset_name: str, docset_version: str, feeds_dir: str, docset_dir: str = config.docset_dir) -> None:
    """Download a docset by its feed name.

    :param docset_name: String, the feed name of the docset to download
    :param docset_version: String, the docset version to download
    :param feeds_dir: String, the feeds directory - use get_feeds() to create it and get its location.
    :param docset_dir: String, the directory Zeal reads docsets from. Default: filesystem.docset_dir
    :return: None
    """
    # Get docset xml file
    docset_xml_path = _get_docset_xml(docset_name, feeds_dir)

    # Extract the URL and download it to the docset dir
    with open(docset_xml_path, "r") as file:
        file_contents = file.read()
        soup = bs4.BeautifulSoup(file_contents, "lxml")
        urls = soup.find_all("url")
        url = urls[0].getText()
        # Adjust URL if version is specified
        if docset_version is not None:
            # Verify if version is available in feed
            if soup.find("other-versions") and soup.findAll(text=docset_version):
                parsed_uri = urllib.parse.urlparse(url)
                file_name = os.path.basename(parsed_uri.path)
                url = f"{parsed_uri.scheme}://{parsed_uri.netloc}/feeds/zzz/versions/{docset_name}/{docset_version}/{file_name}"
            else:
                raise exceptions.DocsetNotExistsError(
                    f"Version {docset_version} does not exist for {docset_name}"
                )

    downloads.download_and_extract(url, docset_dir)


def remove(docset_name: str, docset_dir: str = config.docset_dir):
    """

    :param docset_name: String, the name of the docset to remove
    :param docset_dir: Optional: String, the path to the docset directory. Default: filesystem.docset_dir
    :return:
    """
    if docset_name not in list_all(docset_dir=docset_dir):
        raise exceptions.DocsetNotInstalledError(
            f"The docset to remove '{docset_name}' cannot be removed because it is not installed on your system."
        )
    shutil.rmtree(os.path.join(docset_dir, f"{docset_name}.docset"))


def get_docset_versions(docset_name: str, feeds_dir: str):
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


def _get_docset_xml(docset_name: str, feeds_dir: str):
    """Returns the correct docset xml file

    :param docset_name: String, the name of the docset to remove
    :param feeds_dir: String, the feeds directory - use get_feeds() to create it and get its location.
    :return: the docset xml file path
    """
    # Get a list of docset .xml files
    available_docsets = set()
    for file in os.listdir(feeds_dir):
        if file.endswith(".xml"):
            available_docsets.add(file)

    # Find the correct docset .xml file
    docset_xml_path = None
    for file in available_docsets:
        if file.startswith(docset_name):
            docset_xml_path = os.path.join(feeds_dir, file)
            break
    if docset_xml_path is None:
        raise exceptions.DocsetNotExistsError(
            f"The docset '{docset_name}' cannot be found in the feeds to download."
        )
    
    return docset_xml_path