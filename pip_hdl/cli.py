"""pip-hdl command line helper utility."""

import argparse
import sys
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Sequence

from packaging.requirements import Requirement

from .graph import DependencyGraph
from .metainfo import PackageMetaInfo
from .version import __version__


class _CliCommands(str, Enum):
    """CLI command to invoke."""

    INSPECT = "inspect"


class _CliInspectCmd(str, Enum):
    """Specify target for inspect operation."""

    FILELIST = "filelist"
    SOURCES_ROOT = "sources_root"
    SOURCES_VAR = "sources_var"
    ALL_FILELISTS = "all_filelists"
    ALL_FILELISTS_AS_ARGS = "all_filelists_as_args"
    ALL_SOURCES_ROOTS = "all_sources_roots"
    ALL_SOURCES_VARS = "all_sources_vars"
    DEPENDENCY_GRAPH = "dependency_graph"


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
    inspect - inspect meta-information of the provided package or requirements.txt

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
avaliable attributes for inspection:
    filelist              - show absolute path to filelist
    sources_root          - show absolute path to sources root
    sources_var           - show environment variable to setup sources root (in NAME=VAL format)
    all_filelists         - show all filelists in the dependency-resolved order
    all_filelists_as_args - show all filelists as above, but format them as EDA arguments (with -f)
    all_sources_roots     - show absolute paths to all sources directories
    all_sources_vars      - show all environment variables for all sources
    dependency_graph      - dump dependency graph as in image (graphviz required)
"""
        subparser.add_argument(
            metavar="OBJ",
            type=str,
            dest="obj",
            help="object for inspection: name of pip-hdl-powered package or requirements.txt with such packages",
        )

        subparser.add_argument(
            metavar="ATTR",
            type=_CliInspectCmd,
            choices=[e.value for e in _CliInspectCmd],
            dest="attr",
            help="attribute to inspect (list of available attributes is above)",
        )

    def parse_args(  # type: ignore
        self,
        args: Optional[Sequence[str]] = None,
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


def _do_inspect(obj: str, attr: _CliInspectCmd) -> None:
    """Do `inspect` command."""
    if Path(obj).exists():
        with Path(obj).open("r") as f:
            packages = [PackageMetaInfo(Requirement(line).name) for line in f.readlines()]
    else:
        packages = [PackageMetaInfo(obj)]
    graph = DependencyGraph(packages)

    if attr == _CliInspectCmd.FILELIST:
        print(packages[0].filelist)
    elif attr == _CliInspectCmd.SOURCES_ROOT:
        print(packages[0].sources_root)
    elif attr == _CliInspectCmd.SOURCES_VAR:
        var = packages[0].sources_var
        print(f"{var.name}={var.value}")
    elif attr == _CliInspectCmd.ALL_FILELISTS:
        print(" ".join([str(p.metainfo.filelist) for p in graph]))
    elif attr == _CliInspectCmd.ALL_FILELISTS_AS_ARGS:
        print("-f " + " -f ".join([str(p.metainfo.filelist) for p in graph]))
    elif attr == _CliInspectCmd.ALL_SOURCES_ROOTS:
        print(" ".join([str(p.metainfo.sources_root) for p in graph]))
    elif attr == _CliInspectCmd.ALL_SOURCES_VARS:
        print(" ".join([f"{p.metainfo.sources_var.name}={p.metainfo.sources_var.value}" for p in graph]))
    elif attr == _CliInspectCmd.DEPENDENCY_GRAPH:
        result = graph.render(cleanup=True, format="png", outfile=f"{Path(obj).stem}_graph.png")
        print(result.resolve())
    else:
        raise ValueError(f"Attribute '{attr.value}' is not supported yet!")
