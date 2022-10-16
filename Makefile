.PHONY: build linux-install

build:
	poetry run python ./build_system/update_version.py
	poetry run pyinstaller --onefile ./src/zeal_cli/__init__.py --name zeal-cli

linux-install:
	poetry install
	rm ~/.local/bin/zeal-cli
	make build
	chmod +x ./dist/zeal-cli
	cp ./dist/zeal-cli ~/.local/bin/zeal-cli
