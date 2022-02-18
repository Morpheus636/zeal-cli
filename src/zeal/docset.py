import os

import bs4

from . import downloads, filesystem


def download(docset_name: str, feeds_dir: str, docset_dir: str = filesystem.docset_dir) -> None:
    """Download a docset by its feed name.

    :param docset_name: String, the feed name of the docset to downloadf
    :param feeds_dir: String, the feeds directory - use get_feeds() to create it and get its location.
    :param docset_dir: String, the directory Zeal reads docsets from. Default: filesystem.docset_dir
    :return: None
    """
    # Get a list of docset .xml files
    available_docsets = set()
    for file in os.listdir(feeds_dir):
        if file.endswith(".xml"):
            available_docsets.add(file)

    # Find the correct docset .xml file
    for file in available_docsets:
        if file.startswith(docset_name):
            docset_xml_path = os.path.join(feeds_dir, file)
            break

    # Extract the URL and download it to the docset dir
    with open(docset_xml_path, "r") as file:
        file_contents = file.read()
        soup = bs4.BeautifulSoup(file_contents, "lxml")
        urls = soup.find_all("url")
        url = urls[0].getText()
        print(url)
    downloads.download_and_extract(url, docset_dir)


def list_all(docset_dir: str = filesystem.docset_dir) -> list:
    """List the docsets in the docset_dir.

    :param docset_dir: String, path to the Zeal docset directory. DefaultL filesystem.docset_dir
    :return: List of docsets (by name, not by path)
    """
    files_list = os.listdir(docset_dir)
    installed_docsets = []
    for file in files_list:
        if file.endswith(".docset"):
            installed_docsets.append(file.rstrip(".docset"))
    return installed_docsets
