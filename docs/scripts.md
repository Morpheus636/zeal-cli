# Scripts
### `poetry run black <path>`
Runs the Black code formatter on whatever file or directory you pass to it as `<path>`.

For more usage instructions, use `poetry run black -h`

This is run automatically on any files you change using pre-commit, and on all
files during a pull request.

### `poetry run flake8`
Runs flake8.

For more usage instructions, use `poetry run flake8 -h`

This is run automatically on any files you change using pre-commit, and on all files
during a pull request.

### `poetry run isort`
Runs isort, which automatically sorts your imports, and separates them by sections
and type.

For more usage instructions, use `poetry run isort -h`

This is run automatically on any files you change using pre-commit, and on all files
during a pull request.

### `poetry run pytest`
Runs pytest, which runs all of the tests for the project and tells you what problems
arise. 

For more usage instructions, use `poetry run pytest -h`

This is run automatically using pre-commit, and during pull requests.