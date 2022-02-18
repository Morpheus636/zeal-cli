import os
import sys
import tempfile


sys.path.append(os.path.relpath(__file__) + "/../src")
import src.zeal  # NOQA: E402


def test_list_docsets():
    with tempfile.TemporaryDirectory() as docset_dir:
        os.mkdir(os.path.join(docset_dir, "docset1.docset"))
        os.mkdir(os.path.join(docset_dir, "docset2.docset"))
        os.mkdir(os.path.join(docset_dir, "docset3.docset"))
        os.mkdir(os.path.join(docset_dir, "not_a_docset"))
        docset_list = src.zeal.list_docsets.get_list(docset_dir=docset_dir)
        assert "docset1" in docset_list
        assert "docset2" in docset_list
        assert "docset3" in docset_list
        assert "not_a_docset" not in docset_list
