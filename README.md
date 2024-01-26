# pip-hdl

[![Tests & Checks](https://github.com/esynr3z/pip-hdl/actions/workflows/test.yml/badge.svg)](https://github.com/esynr3z/pip-hdl/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/pip-hdl.svg)](https://badge.fury.io/py/pip-hdl)

Most modern programming languages provide package managers to facilitate code reuse, dependency tracking, installation, etc. However, there is no such a standart thing for HDL languages such as SystemVerilog. There are some projects that try to solve this like well-known [FuseSoc](https://github.com/olofk/fusesoc) creating such system from scratch. But what if we try to solve this another way by reusing existing package manager?

`pip-hdl` enables package managing for HDL (e.g. SystemVerilog) VIP or IP cores using Python [pip](https://pip.pypa.io/en/stable/). `pip` is simple and friendly, it allows to create quite lightweight packages, which are easy to publish to [PyPi](https://pypi.org/) or your local index, and install.

*DICLAIMER: this project has not used in production or tested properly yet, it is better described as Proof-of-Concept at this point.*

## How to install `pip-hdl`

The simplest ways is just use pip as for any other Python package:

```bash
python -m pip install pip-hdl
```

To facilitate package managing process consider installing [poetry](https://python-poetry.org/) as well:

```bash
python -m pip install poetry
```

All the examples and the guide below use it. However, packaging and publishing can be done in [other ways](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for sure.

## How to create a package

Run `pip-hdl new` and follow the interactive instructions. Refer [examples](example/dummy_math_lib) to get an idea how a result looks like - only several files with 5-10 lines of code are required.

Flow in a nutshell:

- Create a filelist (`.f` file) for your HDL component. It should contain all needed information to compile in EDA: include directories, defines and sources.
- Put your component into Python package (basically directory with `__init__.py`). And add some meta information to your package.
- Build and publish!

Check out the guide section below to get more details.

## How to use a package

Run `pip install <name>` to get a package and then put `pip-hdl inspect <name> <attr>` calls into your scripts to get all the required information for compilation (paths, environment variables, etc.).

Check out the guide section below to get more details.

## Guide

### Create HDL component

What HDL code can be packed? Actually, any piece of code which can be described as a single compilation unit via filelist.

Use of filelists aka `.f` files is a common way in EDA world to describe compilation attributes for a single component. As the name suggests, `.f` is list of source files to be compiled. Usually, it also consists of include directories and possibly defines. All the things above are described almost equal in the most EDA tools, so filelists are pretty universal.

To make your HDL component `pip` and `pip-hdl` compatible simple requirements have to followed:

-  All sources and filelists have to be placed within Python package directory to be packed (directory with `__init__.py`). This directory would be the *root directory* for your sources.
- There should be `filelist.f` in the sources root. This is an "entry point" discoverable by `pip-hdl` to help you compile and simulate your component later.
- All directories and sources mentioned within filelist have to use environment variable `${<PACKAGENAME>_SOURCES_ROOT}`. In other words all paths are absolute and based on a path to your sources root.
- If your component depends on another one, then *do not* mention any sources or filelists of that component in your `filelist.f`. Instead, you need to correctly fill metadata of a package and use `pip-hdl` introspection possibilities to get all required fileslists in the correct order for your component and dependencies.

### Add package metadata

To be successfully packed any Python package has to carry some portion of metadata. There are several ways to do it, but in general it ends up in filling [pyproject.toml file](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/) nearby a package.
This file usually includes: package name and version, author name, list of dependencies, and some metadata for packaging backend. Check out [one of such files in examples](example/fizzbuzz_agent/pyproject.toml).

Also `pip-hdl` adds a bit above to ease HDL components management. This additional metadata is stored inside the package, and can be added by these two lines within `__init__.py`:

```python
from pip_hdl import PackageMetaInfo
metainfo = PackageMetaInfo("package_name")
```

*Note, that `pip-hdl` always expects that your package has `metainfo` variable of type `PackageMetaInfo` inside.*

### Pack and publish package

Python package management system a bit messed up, as [Python environment](https://xkcd.com/1987/) and other things, therefore you have a lot of options. Check out [this tutorial](https://packaging.python.org/en/latest/tutorials/packaging-projects/) to get an idea how package could be published.

`pip-hdl` is implicitly expects [poetry](https://python-poetry.org/) use and publishing process in this system is pretty straightforward:

```bash
poetry build
poetry publish
```

You can also check out [CI publish.yml script](.github/workflows/publish.yml) of this repository to get an idea how `pip-hdl` is published via `poetry` itself.

### Install package

Your package and its dependencies can be installed from an index:

```
python -m pip install <package_name>
```

Or from a [.whl file](https://peps.python.org/pep-0427/)

```
python -m pip install <distribution_name>.whl
```

Or as a part of packages listed in [requirements.txt](https://pip.pypa.io/en/stable/user_guide/#requirements-files)

```
python -m pip install -r requirements.txt
```

### Get package metadata

`pip-hdl` allows to get package attributes printed via `inspect` command. Output can be used within your Makefile, bash or other script.

```bash
$ pip-hdl inspect -h
usage: pip-hdl inspect [-h] OBJ ATTR

avaliable attributes for inspection:
    filelist              - show absolute path to filelist
    sources_root          - show absolute path to sources root
    sources_var           - show environment variable to setup sources root (in NAME=VAL format)
    all_filelists         - show all filelists in the dependency-resolved order
    all_filelists_as_args - show all filelists as above, but format them as EDA arguments (with -f)
    all_sources_roots     - show absolute paths to all sources directories
    all_sources_vars      - show all environment variables for all sources
    dependency_graph      - dump dependency graph as in image (graphviz required)

positional arguments:
  OBJ         object for inspection: name of pip-hdl-powered package or requirements.txt with such packages
  ATTR        attribute to inspect (list of available attributes is above)
```

Options are quite self-descriptive, but you can also refer [an example Makefile](example/testbench/Makefile).

Alternative way of getting the same metadata is to use Python:

```python
import fizzbuzz_agent
print(fizzbuzz_agent.metadata.filelist)
```
