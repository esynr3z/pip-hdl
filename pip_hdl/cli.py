"""pip-hdl command line interface.

This CLI helps to inspect metainformation details without extra Python code.
"""

import argparse
import sys
from enum import Enum
from typing import Any, Sequence

from .version import __version__
from .metainfo import PackageMetaInfo


class CliCommands(str, Enum):
    """CLI command to invoke."""

    INSPECT = "inspect"


class CliInspectTarget(str, Enum):
    """Specify target for inspect operation."""

    FILELIST = "filelist"
    ALL_FILELISTS = "all_filelists"
    ALL_FILELISTS_AS_ARGS = "all_filelists_as_args"
    SOURCES_DIR = "sources_dir"
    ALL_SOURCES_DIRS = "all_sources_dirs"
    SOURCES_VAR = "sources_var"
    ALL_SOURCES_VARS = "all_sources_vars"


class ArgumentParser(argparse.ArgumentParser):
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
            dest="object",
            help=f"object for inspection: name of pip-hdl-powered package or requirements.txt with such packages",
        )

        subparser.add_argument(
            metavar="ATTR",
            type=CliInspectTarget,
            choices=[e.value for e in CliInspectTarget],
            dest="attr",
            help=f"attribute to inspect (list of available attributes is above)",
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
        ns.cmd = CliCommands(ns.cmd)  # cast to enum

        return ns


def enter_cli() -> None:
    """Enter CLI application."""
    parser = ArgumentParser(prog="pip-hdl")
    parser.configure()
    args = parser.parse_args()


"""
    if args.mode == CliMode.FILELIST:
        print(metainfo.filelist)
    elif args.mode == CliMode.SOURCES_DIR:
        print(metainfo.sources_dir)
    elif args.mode == CliMode.SOURCES_VAR:
        var = metainfo.sources_var
        print(f"{var.name}={var.value}")
    elif args.mode == CliMode.ALL_SOURCES_VARS:
        print(" ".join([f"{var.name}={var.value}" for var in metainfo.all_sources_vars]))
    else:
        raise RuntimeError("Unknown mode!")
"""
