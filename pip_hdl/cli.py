"""HDL package CLI.

This CLI helps to inspect metainformation details without extra Python code.
"""

import argparse
import sys
from enum import Enum
from typing import Any, Sequence

from .metainfo import PackageMetaInfo


class CliMode(str, Enum):
    """Specify CLI mode or what to inspect."""

    FILELIST = "filelist"
    SOURCES_DIR = "sources_dir"
    SOURCES_VAR = "sources_var"
    ALL_SOURCES_VARS = "all_sources_vars"


class ArgumentParser(argparse.ArgumentParser):
    """CLI argument parser."""

    def __init__(self, prog: str, **kwargs: Any) -> None:
        """Init parser."""
        super().__init__(prog=prog, **kwargs)

        self.add_argument(
            metavar="MODE",
            type=CliMode,
            choices=[e.value for e in CliMode],
            dest="mode",
            help=f"choose operational mode for cli, choices: {', '.join([e.value for e in CliMode])}",
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
        return ns


def enter_package_cli(metainfo: PackageMetaInfo) -> None:
    """Enter CLI for the provided package."""
    parser = ArgumentParser(prog=metainfo.name)
    args = parser.parse_args()

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
