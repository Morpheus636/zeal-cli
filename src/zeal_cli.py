import argparse
import shutil

import zeal


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    install_command = subparsers.add_parser("install")
    install_command.add_argument("docsets", nargs="*")

    subparsers.add_parser("list")

    remove_command = subparsers.add_parser("remove")
    remove_command.add_argument("docsets", nargs="*")

    args = parser.parse_args()

    if args.action == "install":
        print("Getting list of available docsets")
        feeds = zeal.downloads.get_feeds()
        for docset in args.docsets:
            print(f"Installing docset: {docset}")
            zeal.docset.download(docset, feeds)
            print(f"Successfully installed docset: {docset}")
        print("Cleaning up")
        shutil.rmtree(feeds)
        print("Done")

    if args.action == "list":
        print(*zeal.docset.list_all(), sep="\n")
    if args.action == "remove":
        for docset in args.docsets:
            print(f"Removing docset: {docset}")
            zeal.docset.remove(docset)
            print(f"Successfully removed docset: {docset}")


if __name__ == "__main__":
    main()
