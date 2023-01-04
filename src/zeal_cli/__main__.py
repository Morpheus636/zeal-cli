import argparse
import shutil
import sys

from . import zeal


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="action")

    install_command = subparsers.add_parser(
        "install", help="Install one or more docsets. See `zeal-cli install --help`"
    )
    install_command.add_argument(
        "docsets",
        nargs="*",
        help=(
            "A list of docset names, separated by a space. "
            "A specific version of a docset can be selected for installation by following "
            "the docset name with an equals (=) and the version of the docset to select"
        ),
    )

    subparsers.add_parser("list", help="Prints a list of installed docsets")

    search_command = subparsers.add_parser("search", help="Prints a list of installed docsets")
    search_command.add_argument("docset", nargs=1, help="A name of a docset.")

    remove_command = subparsers.add_parser(
        "remove", help="Delete one or more docsets. See `zeal-cli remove --help`"
    )
    remove_command.add_argument(
        "docsets", nargs="*", help="A list of docset names, separated by a space."
    )

    config_command = subparsers.add_parser(
        "config", help="View or edit zeal-cli's configuration. See `zeal-cli config --help`"
    )
    config_command_subparsers = config_command.add_subparsers(dest="config_action")
    config_find_command = config_command_subparsers.add_parser(  # NOQA: F841
        "locate", help="Print the path to the config file."
    )
    config_view_command = config_command_subparsers.add_parser(
        "view", help="Print the current config."
    )
    config_view_command.add_argument(
        "name",
        help="The name of the config value to print. If not specified, prints all config values.",
        nargs="?",
    )
    config_reset_command = config_command_subparsers.add_parser(  # NOQA: F841
        "reset", help="Reset the config to default."
    )
    config_set_command = config_command_subparsers.add_parser(
        "set", help="Change the value of a config field. See `zeal-cli config set --help`"
    )
    config_set_command.add_argument("name", help="The name of the config value to set.")
    config_set_command.add_argument(
        "value", help="The value to assign to the specified config item."
    )

    parser.add_argument(
        "-v", "--version", action="store_true", help="Print Zeal-CLI's version information"
    )

    args = parser.parse_args()

    if args.version:
        print(f"Build Version: {zeal.version.build_version}")
        sys.exit()
    if args.action == "install":
        if args.docsets:
            print("Getting list of available docsets")
            feeds = zeal.downloads.get_feeds()
            for docset in args.docsets:
                docset_name = docset
                docset_version = zeal.docset.LATEST_VERSION
                # Parse version string if defined
                if "=" in docset:
                    docset_info = docset.split("=", 1)
                    docset_name = docset_info[0]
                    docset_version = docset_info[1]
                print(f"Installing docset: {docset}")
                zeal.docset.download(docset_name, feeds, docset_version=docset_version)
                print(f"Successfully installed docset: {docset}")
            print("Cleaning up")
            shutil.rmtree(str(feeds.resolve()))
            print("Done")
        else:
            install_command.print_help()

    elif args.action == "list":
        print(*zeal.docset.list_all(), sep="\n")

    elif args.action == "search":
        feeds = zeal.downloads.get_feeds()
        docset_name = args.docset[0]
        docset_versions = zeal.docset.get_docset_versions(docset_name, feeds)
        print(f"Available versions for docset {docset_name}: {', '.join(docset_versions)}")

    elif args.action == "remove":
        if args.docsets:
            for docset in args.docsets:
                print(f"Removing docset: {docset}")
                zeal.docset.remove(docset)
                print(f"Successfully removed docset: {docset}")
        else:
            remove_command.print_help()

    elif args.action == "config":
        if args.config_action == "locate":
            print(zeal.config.cli_config_path)
        elif args.config_action == "view":
            if args.name:
                print(zeal.config.cli_config[args.name])
            else:
                print(zeal.config.cli_config)
        elif args.config_action == "reset":
            zeal.config.set_default_config(zeal.config.cli_config_path)
        elif args.config_action == "set":
            zeal.config.set_config_value(args.name, args.value, zeal.config.cli_config_path)
        else:
            config_command.print_help()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
