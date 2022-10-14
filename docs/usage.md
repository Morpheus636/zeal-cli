# Usage
Right now, Zeal_CLI only supports Linux.

# Installation

## Linux - Pre Built
1. Download the linux build from the most recent [release](https://github.com/Morpheus636/zeal_cli/releases)
3. Copy the linux build to `~/.local/bin` (or another location on PATH)
4. Give the file executable permissions (`chmod +x ~/.local/bin/zeal-cli`)
6. Run it with `zeal-cli`

## Linux - From Source
1. Clone this repo using Git - `git clone https://github.com/Morpheus636/zeal-cli.git`
2. Checkout the repo at the most recent version tag (or branch) - `git checkout tags/<tag_name>` or `git checkout origin/<branch_name>`
3. Run `make clean` (May not be nessesary if its your first time building zeal-cli, but won't hurt)
4. Run `make linux-install`

## Usage
Usage information can be found by running `zeal-cli --help`
