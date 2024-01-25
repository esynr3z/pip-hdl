# Example

Simple example of how to pack and use packed components to build a testbench.

- `dummy_math_lib` - root directory for `dummy_math_lib` package
- `fizzbuzz_agent` - root directory for `fizzbuzz_agent` package, which depends on `dummy_math_lib`
- `testbench` - directory with testbench using `fizzbuzz_agent`

Normally, to run testbench you simply need to install all dependencies using

```bash
pip install -r requirements.txt
```

However, mentioned packages are protected from publishing to PyPi with the special [trove classifier](https://pypi.org/classifiers/), but you still can pack and install them locally.

Make sure that you have [poetry](https://python-poetry.org/) installed:

```bash
pip install poetry
```

Then you can build [.whl](https://peps.python.org/pep-0427/) and install it to your system:

```bash
cd <package_root>
poetry build
pip install dist/<package>.whl
```

After all packages are installed try to run the testbench in [Verilator](https://www.veripool.org/verilator/) using `make`.
