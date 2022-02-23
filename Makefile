build:
	poetry run pyinstaller --onefile ./src/zeal_cli.py --name zeal-cli

linux-install:
	poetry install
	rm ~/.local/bin/zeal-cli
	poetry run pyinstaller --onefile ./src/zeal_cli.py --name zeal-cli
	chmod +x ./dist/zeal-cli
	cp ./dist/zeal-cli ~/.local/bin/zeal-cli
