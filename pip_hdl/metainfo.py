"""Meta-information for HDL package."""

from __future__ import annotations

import pkgutil
from importlib import import_module, metadata
from pathlib import Path
from types import ModuleType
from typing import List, NamedTuple, Optional

from packaging.requirements import Requirement


class EnvVar(NamedTuple):
    """Environment variable."""

    name: str
    value: str


class PackageDependency(NamedTuple):
    """Descriptor for a HDL package dependency."""

    spec: str  # packaging.requirements.Requirement friendly specification
    module: Optional[ModuleType]
    metainfo: PackageMetaInfo


class PackageMetaInfo:
    """HDL package meta information."""

    # All the HDL packages has to follow this conventions
    SOURCES_VAR_SUFFIX = "SOURCES_ROOT"
    FILELIST_NAME = "filelist.f"

    def __init__(self, py_pkg_name: str) -> None:
        """Init package meta-information."""
        self.name: str = py_pkg_name

        self._dependencies: Optional[List[PackageDependency]] = None
        self._filelist: Optional[Path] = None
        self._sources_root: Optional[Path] = None
        self._sources_var: Optional[EnvVar] = None
        self._all_sources_vars: Optional[List[EnvVar]] = None

    @property
    def dependencies(self) -> List[PackageDependency]:
        """Dependencies of the current package.

        Dependency search is based on the presense of `metainfo` attribute within top-module.
        """
        if self._dependencies is None:
            self._dependencies = []

            required_packages = metadata.requires(self.name)
            if required_packages is not None:
                for spec in required_packages:
                    try:
                        module = import_module(Requirement(spec).name)
                        if isinstance(module.metainfo, PackageMetaInfo):
                            dependency = PackageDependency(spec=spec, module=module, metainfo=module.metainfo)
                            self._dependencies.append(dependency)
                    except (ImportError, AttributeError) as _:  # noqa
                        pass
        return self._dependencies

    @property
    def filelist(self) -> Path:
        """Path to an EDA filelist."""
        if self._filelist is None:
            pkg_loader = pkgutil.get_loader(self.name)
            if pkg_loader is None:
                raise ModuleNotFoundError(f"Can't find package '{self.name}'. It has to be installed.")

            pkg_root = Path(pkg_loader.get_filename()).parent  # type: ignore
            pkg_filelist = pkg_root / self.FILELIST_NAME

            if not pkg_filelist.exists():
                raise FileNotFoundError(
                    f"{self.FILELIST_NAME} was not found within '{self.name}' component at {pkg_root}!"
                    " Is this correct package?"
                )

            self._filelist = pkg_filelist
        return self._filelist

    @property
    def sources_root(self) -> Path:
        """Path to a directory with HDL sources."""
        if self._sources_root is None:
            self._sources_root = self.filelist.parent
        return self._sources_root

    @property
    def sources_var(self) -> EnvVar:
        """Environment variable for directory with sources."""
        if self._sources_var is None:
            self._sources_var = EnvVar(f"{self.name.upper()}_{self.SOURCES_VAR_SUFFIX}", str(self.sources_root))
        return self._sources_var
