#!/usr/bin/env python3

"""
Dummy script to setup a project from the template
"""

import os
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint


@dataclass
class Project:
    name: str
    author: str
    description: str
    github_user: str
    github_repo: str


def replace_in_file(file: Path, old: str, new: str) -> None:
    with file.open("r") as f:
        lines = []
        for line in f.readlines():
            lines.append(line.replace(old, new))
    with file.open("w") as f:
        f.writelines(lines)


def query_config() -> Project:
    return Project(
        name=input("> Name of the project?\n"),
        description=input("> Short description?\n"),
        author=input("> Author?\n"),
        github_user=input("> Github username?\n"),
        github_repo=input("> Github repository name?\n"),
    )


def apply_config(config: Project) -> None:
    template = Project(
        name="template_python_project",
        author="johnsmith <johnsmith@mail.com>",
        description="project_description",
        github_user="johnsmith",
        github_repo="template-python-project",
    )
    os.rename(template.name, config.name)
    replace_in_file(Path("tests/test_version.py"), template.name, config.name)
    replace_in_file(Path("LICENSE"), template.author, config.author)

    replace_in_file(Path("pyproject.toml"), template.name, config.name)
    replace_in_file(Path("pyproject.toml"), template.description, config.description)
    replace_in_file(Path("pyproject.toml"), template.author, config.author)
    replace_in_file(Path("pyproject.toml"), template.github_user, config.github_user)
    replace_in_file(Path("pyproject.toml"), template.github_repo, config.github_repo)

    replace_in_file(Path("tox.ini"), template.name, config.name)

    replace_in_file(Path("README.md"), template.name, config.name)
    replace_in_file(Path("README.md"), template.github_user, config.github_user)
    replace_in_file(Path("README.md"), template.github_repo, config.github_repo)


if __name__ == "__main__":
    config = query_config()
    print("Provided configuration:")
    pprint(config)

    while True:
        apply = input("> Apply configuration? y/n\n")
        if apply == "y":
            apply_config(config)
            break
        elif apply == "n":
            break
    print("Done!")
