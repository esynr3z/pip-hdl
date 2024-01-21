"""Meta-information for HDL package."""

from __future__ import annotations

import pkgutil
from importlib import metadata
from pathlib import Path
from typing import List, NamedTuple, Optional

from packaging.requirements import Requirement


class EnvVar(NamedTuple):
    """Environment variable."""

    name: str
    value: str


class PackageMetaInfo:
    """HDL package meta information."""

    # All the HDL packages has to follow this conventions
    SOURCES_VAR_SUFFIX = "SOURCES_ROOT"
    FILELIST_NAME = "filelist.f"

    def __init__(self, py_pkg_name: str) -> None:
        """Init package meta-information."""
        self.name: str = py_pkg_name

        self._dependencies: Optional[List[PackageMetaInfo]] = None
        self._filelist: Optional[Path] = None
        self._sources_dir: Optional[Path] = None
        self._sources_var: Optional[EnvVar] = None
        self._all_sources_vars: Optional[List[EnvVar]] = None

    @property
    def dependencies(self) -> List[PackageMetaInfo]:
        """Dependencies of the current package.

        Dependencies search is based on the presense of filelist.
        """
        if self._dependencies is None:
            self._dependencies = []

            required_packages = metadata.requires(self.name)
            if required_packages is not None:
                for spec in required_packages:
                    req = Requirement(spec)
                    req_metainfo = PackageMetaInfo(req.name)
                    try:
                        req_metainfo.filelist
                        self._dependencies.append(req_metainfo)
                    except FileNotFoundError:
                        pass
        return self._dependencies

    @property
    def filelist(self) -> Path:
        """Path to an EDA filelist."""
        if self._filelist is None:
            pkg_loader = pkgutil.get_loader(self.name)
            if pkg_loader is None:
                raise FileNotFoundError(f"Can't find package '{self.name}'")

            pkg_root = Path(pkg_loader.get_filename()).parent  # type: ignore
            pkg_filelist = pkg_root / self.FILELIST_NAME

            if not pkg_filelist.exists():
                raise FileNotFoundError(
                    f"{self.FILELIST_NAME} was not found within '{self.name}' component at {pkg_root}!"
                )

            self._filelist = pkg_filelist
        return self._filelist

    @property
    def sources_dir(self) -> Path:
        """Path to a directory with HDL sources."""
        if self._sources_dir is None:
            self._sources_dir = self.filelist.parent
        return self._sources_dir

    @property
    def sources_var(self) -> EnvVar:
        """Environment variable for directory with sources."""
        if self._sources_var is None:
            self._sources_var = EnvVar(f"{self.name.upper()}_{self.SOURCES_VAR_SUFFIX}", str(self.sources_dir))
        return self._sources_var

    @property
    def all_sources_vars(self) -> List[EnvVar]:
        """Environment variables for all sources, including dependencies first."""
        if self._all_sources_vars is None:
            self._all_sources_vars = []
            for d in self.dependencies:
                self._all_sources_vars.extend(d.all_sources_vars)
            self._all_sources_vars.append(self.sources_var)
        return self._all_sources_vars
