"""Templating utilities."""

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Dict, Any

from .version import __version__


@dataclass
class TemplateConfig:
    """Configuration for a template."""

    package_name: str
    package_description: str
    author_name: str
    is_private_package: bool


def ask_user_for_string(question: str, default_answer: Optional[str] = None) -> str:
    """Ask user to get a string value."""
    default_note = "" if default_answer is None else f" (default: '{default_answer}')"
    answer = input(f"> {question}{default_note}\n").strip()
    if (answer == "") and (default_answer is not None):
        return default_answer
    else:
        return answer


def ask_user_for_bool(question: str, default_answer: Optional[bool] = None) -> bool:
    """Ask user to get a boolean answer."""
    yes_opt = "Y" if default_answer is True else "y"
    no_opt = "N" if default_answer is False else "n"
    while True:
        answer = input(f"> {question} {yes_opt}/{no_opt}\n").strip()
        if answer.lower().startswith("y"):
            return True
        elif answer.lower().startswith("n"):
            return False
        elif answer == "" and (default_answer is not None):
            return default_answer


def ask_user_for_config() -> TemplateConfig:
    """Ask user questions to create template configuration interactively."""
    cfg: Dict[str, Any] = {
        "package_name": ask_user_for_string("Python package name?"),
        "package_description": ask_user_for_string("Python package description?", default_answer=""),
        "author_name": ask_user_for_string("Author name? Format: John Doe <johndoe@mail.com>)"),
        "is_private_package": ask_user_for_bool("Protect package from publishing to PyPi?", default_answer=False),
    }
    return TemplateConfig(**cfg)


def template_package_example(outdir: Path, cfg: TemplateConfig) -> None:
    """Create an example of SV package."""
    # FIXME: current version is quite ugly, consider switching to more straighforward way of templating
    # using files and maybe jinja
    print("Create files and directories:")

    project_root = outdir / cfg.package_name
    shutil.rmtree(project_root, ignore_errors=True)
    project_root.mkdir(parents=True)
    print(project_root)

    package_root = project_root / cfg.package_name
    package_root.mkdir()
    print(package_root)

    print(_create_init_py(package_root, cfg))
    print(_create_pkg_sv(package_root, cfg))
    print(_create_filelist_f(package_root, cfg))
    print(_create_pyproject_toml(project_root, cfg))


def _create_init_py(outdir: Path, cfg: TemplateConfig) -> Path:
    """Create __init__.py for the example project."""
    init_py_file = outdir / "__init__.py"
    init_py_text = f'''"""{cfg.package_name}."""
from pip_hdl import PackageMetaInfo

metainfo = PackageMetaInfo("{cfg.package_name}")
'''
    with init_py_file.open("w") as f:
        f.write(init_py_text)
    return init_py_file


def _create_pkg_sv(outdir: Path, cfg: TemplateConfig) -> Path:
    """Create SV package for the example project."""
    pkg_sv_file = outdir / f"{cfg.package_name}_pkg.sv"
    pkg_sv_text = f"""package {cfg.package_name}_pkg;
endpackage
"""
    with pkg_sv_file.open("w") as f:
        f.write(pkg_sv_text)
    return pkg_sv_file


def _create_filelist_f(outdir: Path, cfg: TemplateConfig) -> Path:
    """Create filelist.f for the example project."""
    filelist_f_file = outdir / "filelist.f"
    filelist_f_text = f"""${{{cfg.package_name.upper()}_SOURCES_ROOT}}/{cfg.package_name}_pkg.sv
"""

    with filelist_f_file.open("w") as f:
        f.write(filelist_f_text)
    return filelist_f_file


def _create_pyproject_toml(outdir: Path, cfg: TemplateConfig) -> Path:
    """Create pyproject.toml for the example project."""
    private_classifier = """classifiers = [
    "Private :: Do not Upload", # Prevent uploading to PyPI
]
"""
    pyproject_toml_file = outdir / "pyproject.toml"
    pyproject_toml_text = f"""[tool.poetry]
name = "{cfg.package_name.replace("_", "-")}"
version = "0.1.0"
description = "{cfg.package_description}"
authors = ["{cfg.author_name}"]
{private_classifier if cfg.is_private_package else ''}

[tool.poetry.dependencies]
python = "^3.8"
pip_hdl = "^{__version__}"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
"""
    with pyproject_toml_file.open("w") as f:
        f.write(pyproject_toml_text)
    return pyproject_toml_file
