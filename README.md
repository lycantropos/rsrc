rsrc
====

[![](https://travis-ci.com/lycantropos/rsrc.svg?branch=master)](https://travis-ci.com/lycantropos/rsrc "Travis CI")
[![](https://dev.azure.com/lycantropos/rsrc/_apis/build/status/lycantropos.rsrc?branchName=master)](https://dev.azure.com/lycantropos/rsrc/_build/latest?definitionId=4&branchName=master "Azure Pipelines")
[![](https://codecov.io/gh/lycantropos/rsrc/branch/master/graph/badge.svg)](https://codecov.io/gh/lycantropos/rsrc "Codecov")
[![](https://img.shields.io/github/license/lycantropos/rsrc.svg)](https://github.com/lycantropos/rsrc/blob/master/LICENSE "License")
[![](https://badge.fury.io/py/rsrc.svg)](https://badge.fury.io/py/rsrc "PyPI")

In what follows
- `python` is an alias for `python3.5` or any later
version (`python3.6` and so on),
- `pypy` is an alias for `pypy3.5` or any later
version (`pypy3.6` and so on).

Installation
------------

Install the latest `pip` & `setuptools` packages versions:
- with `CPython`
  ```bash
  python -m pip install --upgrade pip setuptools
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade pip setuptools
  ```

### User

Download and install the latest stable version from `PyPI` repository:
- with `CPython`
  ```bash
  python -m pip install --upgrade rsrc
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --upgrade rsrc
  ```

### Developer

Download the latest version from `GitHub` repository
```bash
git clone https://github.com/lycantropos/rsrc.git
cd rsrc
```

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements.txt
  ```

Install:
- with `CPython`
  ```bash
  python setup.py install
  ```
- with `PyPy`
  ```bash
  pypy setup.py install
  ```

Usage
-----

The main idea is to use `setuptools` feature 
called ["Dynamic Discovery of Services and Plugins"](https://setuptools.readthedocs.io/en/latest/setuptools.html#dynamic-discovery-of-services-and-plugins).

Assuming we have a package `rsrc_ftp` with structure

    |_ rsrc_ftp.py
    |_ setup.py

which adds support for URLs with `ftp` scheme

`rsrc_ftp.py`
```python
from rsrc.models import Resource

def deserialize(string: str) -> Resource:
    ...
```

to make it available for `rsrc` package 
we should register its entry point 
(`rsrc_ftp::deserialize` function in our case)

`setup.py`
```python
from setuptools import setup

from rsrc import plugins

plugins_entry_points = [
    plugins.to_entry_point(id_=plugins.to_id('ftp'),
                           module_name='rsrc_ftp',
                           function_name='deserialize'),
]
setup(name='rsrc_ftp',
      py_modules=['rsrc_ftp'],
      entry_points={plugins.__name__: plugins_entry_points},
      install_requires=['rsrc'])
```

After that the installation of `rsrc_ftp` package 
will register `rsrc_ftp::deserialize` function in `rsrc` package 
as an entry point for resources with `ftp` scheme

```python
>>> from rsrc.base import deserialize
>>> ftp_resource = deserialize('ftp://path/to/resource')
>>> ftp_resource.url
URL('ftp', 'path', '/to/resource', '', '', '')
```

Plugins
-------

- [`rsrc_local`](https://pypi.org/project/rsrc_local) -- adds support for local/local network resources.
- [`rsrc_web`](https://pypi.org/project/rsrc_web) -- adds support for web resources (both `http` & `https` schemes).

Development
-----------

### Bumping version

#### Preparation

Install
[bump2version](https://github.com/c4urself/bump2version#installation).

#### Pre-release

Choose which version number category to bump following [semver
specification](http://semver.org/).

Test bumping version
```bash
bump2version --dry-run --verbose $CATEGORY
```

where `$CATEGORY` is the target version number category name, possible
values are `patch`/`minor`/`major`.

Bump version
```bash
bump2version --verbose $CATEGORY
```

This will set version to `major.minor.patch-alpha`. 

#### Release

Test bumping version
```bash
bump2version --dry-run --verbose release
```

Bump version
```bash
bump2version --verbose release
```

This will set version to `major.minor.patch`.

#### Notes

To avoid inconsistency between branches and pull requests,
bumping version should be merged into `master` branch 
as separate pull request.

### Running tests

Install dependencies:
- with `CPython`
  ```bash
  python -m pip install --force-reinstall -r requirements-tests.txt
  ```
- with `PyPy`
  ```bash
  pypy -m pip install --force-reinstall -r requirements-tests.txt
  ```

Plain
```bash
pytest
```

Inside `Docker` container:
- with `CPython`
  ```bash
  docker-compose --file docker-compose.cpython.yml up
  ```
- with `PyPy`
  ```bash
  docker-compose --file docker-compose.pypy.yml up
  ```

`Bash` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```bash
  ./run-tests.sh
  ```
  or
  ```bash
  ./run-tests.sh cpython
  ```

- with `PyPy`
  ```bash
  ./run-tests.sh pypy
  ```

`PowerShell` script (e.g. can be used in `Git` hooks):
- with `CPython`
  ```powershell
  .\run-tests.ps1
  ```
  or
  ```powershell
  .\run-tests.ps1 cpython
  ```
- with `PyPy`
  ```powershell
  .\run-tests.ps1 pypy
  ```
