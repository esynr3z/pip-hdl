"""pip-hdl command line interface.

This CLI helps to inspect metainformation details without extra Python code.
"""

import argparse
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Sequence

from .metainfo import PackageMetaInfo
from .version import __version__


class _CliCommands(str, Enum):
    """CLI command to invoke."""

    INSPECT = "inspect"


class _CliInspectTarget(str, Enum):
    """Specify target for inspect operation."""

    FILELIST = "filelist"
    ALL_FILELISTS = "all_filelists"
    ALL_FILELISTS_AS_ARGS = "all_filelists_as_args"
    SOURCES_DIR = "sources_dir"
    ALL_SOURCES_DIRS = "all_sources_dirs"
    SOURCES_VAR = "sources_var"
    ALL_SOURCES_VARS = "all_sources_vars"


class _ArgumentParser(argparse.ArgumentParser):
    """CLI argument parser."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Init parser."""
        if "formatter_class" not in kwargs:
            kwargs["formatter_class"] = argparse.RawTextHelpFormatter
        super().__init__(*args, **kwargs)

    def configure(self) -> None:
        """Configure parser with arguments, subparsers, etc."""
        self.description = """
avaliable commands:
    inspect     - inspect meta-information of the provided object

add -h/--help argument to any command to get more information and specific arguments"""

        self.add_argument(
            "-V",
            "--version",
            action="version",
            version=__version__,
        )

        subparsers = self.add_subparsers(help="cli command", dest="cmd", required=True)
        inspect_subparser = subparsers.add_parser("inspect")
        self._configure_inspect_subparser(inspect_subparser)

    def _configure_inspect_subparser(self, subparser: argparse.ArgumentParser) -> None:
        """Configure subparser for `inspect` command."""
        subparser.description = """
avaliable attributes for package inspection:
    filelist              - show absolute path to filelist
    sources_dir           - show absolute path to sources root
    sources_var           - show environment variable to setup sources root (in NAME=VAL format)

avaliable attributes for requirements.txt inspection:
    all_filelists         - show all filelists in the dependency-resolved order
    all_filelists_as_args - show all filelists as above, but format them as EDA arguments (with -f)
    all_sources_dirs      - show absolute paths to all sources directories
    all_sources_vars      - show all environment variables for all sources
"""
        subparser.add_argument(
            metavar="OBJ",
            type=str,
            dest="obj",
            help="object for inspection: name of pip-hdl-powered package or requirements.txt with such packages",
        )

        subparser.add_argument(
            metavar="ATTR",
            type=_CliInspectTarget,
            choices=[e.value for e in _CliInspectTarget],
            dest="attr",
            help="attribute to inspect (list of available attributes is above)",
        )

    def parse_args(  # type: ignore
        self,
        args: Sequence[str] | None = None,
        namespace: None = None,
    ) -> argparse.Namespace:
        """Parse CLI arguments."""
        if len(sys.argv) < 2:
            # if no arguments, show help and exit
            sys.argv.append("--help")

        ns = super().parse_args(args, namespace)
        ns.cmd = _CliCommands(ns.cmd)  # cast to enum

        return ns


def enter_cli() -> None:
    """Enter CLI of application."""
    parser = _ArgumentParser(prog="pip-hdl")
    parser.configure()
    args = parser.parse_args()

    if args.cmd == _CliCommands.INSPECT:
        _do_inspect(obj=args.obj, attr=args.attr)


def _do_inspect(obj: str, attr: _CliInspectTarget) -> None:
    """Do `inspect` command."""
    if Path(obj).exists():
        raise NotImplementedError("Handler for file with requirements is not implemented yet")
    else:
        metainfo = PackageMetaInfo(obj)
        if attr == _CliInspectTarget.FILELIST:
            print(metainfo.filelist)
        elif attr == _CliInspectTarget.SOURCES_DIR:
            print(metainfo.sources_dir)
        elif attr == _CliInspectTarget.SOURCES_VAR:
            var = metainfo.sources_var
            print(f"{var.name}={var.value}")
        else:
            raise ValueError(f"Attribute '{attr.value}' is not supported for package inspection!")
