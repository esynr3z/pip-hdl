# Development

Project tooling and choices:

* [poetry](https://python-poetry.org/) - packaging and dependency management
* [poetry-dynamic-versioning](https://github.com/mtkennerly/poetry-dynamic-versioning) - dynamic versioning based on tags and commits in git (poetry plugin)
* [poethepoet](https://poethepoet.natn.io/) - project tasks runner that works well with poetry (poetry plugin)
* [tox](https://tox.wiki/en/latest/) - testing automation in different Python environments
* [black](https://github.com/psf/black) - code formatter
* [isort](https://pycqa.github.io/isort/) - imports sorter that works well with black
* [mypy](https://github.com/python/mypy) - static typing checker
* [flake8](https://github.com/pycqa/flake8) - linter for code and docstrings
* docstrings style - [Google](https://google.github.io/styleguide/pyguide.html#s3.8-comments-and-docstrings) ([example](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html))

## Getting Started

Install main development dependencies (poetry+plugins, tox) to your system at once with

```sh
python3 -m pip install -U -r requirements-dev.txt
```

Then use `poetry` to manage all other dependencies in the underlying virtual environment:

```sh
# this step is optional and only required if you want to specify an interpeter explicitly
poetry env use 3.8

# install all dependencies and a project to a virtual environment
poetry install
```

`poetry-dynamic-versioning` temporary substitute current version in sources when the most of `poetry` commands are used, but with `poetry poe` changes are stay on the disk.
This leads to unwanted "diff noise", so consider adding this variable to your environment to restrict allowed commands for dynamic versioning:

```sh
export POETRY_DYNAMIC_VERSIONING_COMMANDS="publish,build,version"
```

## Code quality control

Common development tasks (lint, format, etc.) are collected in `pyproject.toml` file and can be run via `poetry poe <task>`. Run `poetry poe -h` to get a list with available tasks:

```
...
CONFIGURED TASKS
  clean          Clean project directory from temporary files and folders
  test           Run all tests
  test-cov       Run all tests with coverage collection
  lint           Invoke linting checks
  type           Invoke typing checks
  format         Format all Python files
  check-format   Check Python formatting
  pre-commit     Pre-commit routine to ensure code quality
```

## Testing automation

Testing automation in different Python environments can be accomplished with `tox`. Usually, you don't run tox locally, because CI does this for you.
However, some useful commands are described below:

```sh
# install python versions for testing
pyenv install 3.8.6 3.9 3.10 3.11

# run everything (tests on all interpeters, lint check, format check, etc.)
tox run

# list all jobs (environments)
tox l

# run specific environment
# here, tests on python3.11 + lint
tox -e py3.11 lint

# run specific environments under label `aux`: format, lint, type
tox run -m aux
```
