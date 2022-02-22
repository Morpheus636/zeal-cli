build:
	poetry run pyinstaller --onefile ./src/zeal_cli.py --name zeal-cli

linux-install:
	poetry run pyinstaller --onefile ./src/zeal_cli.py --name zeal-cli
	chmod +x ./dist/zeal-cli
	cp ./dist/zeal-cli ~/.local/bin/zeal-cli
