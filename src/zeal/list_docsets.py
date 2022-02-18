import os

from . import filesystem


def get_list(docset_dir: str = filesystem.docset_dir) -> list:
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
