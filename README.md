# pip-hdl

[![Tests & Checks](https://github.com/esynr3z/pip-hdl/actions/workflows/test.yml/badge.svg)](https://github.com/esynr3z/pip-hdl/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/pip-hdl.svg)](https://badge.fury.io/py/pip-hdl)

Most modern programming languages provide package managers to facilitate code reuse, dependency tracking, installation, etc. However, there is no such a standart thing for HDL languages as SystemVerilog. There are some projects that try to solve this like well-known [FuseSoc](https://github.com/olofk/fusesoc), creating such system from scratch. But what if try to solve this another way by reusing existing package manager?

`pip-hdl` enables package managing for HDL (e.g. SystemVerilog) VIP or IP cores using Python [pip](https://pip.pypa.io/en/stable/). `pip` is simple and friendly, it allows to create quite lightweight packages, which are easy to publish to [PyPi](https://pypi.org/) or your local index, and install.

## How to install `pip-hdl`

The simplest ways is just use pip as for any other Python package:

```bash
pip install pip-hdl
```

To facilitate package managing process consider installing [poetry](https://python-poetry.org/) as well:

```bash
pip install poetry
```

All the examples and the guide below use it. However, packaging and publishing can be done in more [traditional way](https://packaging.python.org/en/latest/tutorials/packaging-projects/) for sure.

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

🚧🚧🚧🚧🚧 WORK IN PROGRESS 🚧🚧🚧🚧🚧

### Create HDL component

### Add package metadata

### Build, publish, install

### Get package metadata