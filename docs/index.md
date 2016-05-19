# Punch

[![Build Status](https://travis-ci.org/lgiordani/punch.svg?branch=master)](https://travis-ci.org/lgiordani/punch)
[![Version](https://img.shields.io/pypi/v/punch.svg)](https://github.com/lgiordani/punch)

Update your version while having a drink

## About punch

Punch is a configurable version updater, and you can use to automate the management of your project's version number.

Punch stores the version of your project in its own file. Each time you need to update it, Punch runs through the configured
 files and replaces the old version with the new one. Additionally, Punch may also automatically commit the version change
 on your VCS of choice.

## Installation

Punch is available for both Python 2 and Python 3 through pip. Just create a virtual environment and run

``` sh
pip install punch
```

To start working with Punch you need a configuration file and a version file. You may ask Punch to create the two files for you with
 reasonable starting values with the flag `--init`
 
``` sh
punch --init
```

which will create the `punch_config.py` and `punch_version.py` files in the current directory. These names are used by default
by Punch, but you may change them (see later).

## Command line options

Punch may be invoked with the following command line options

* `-c`, `--config_file`: If you name your config file differently you may tell Punch here to load that file instead of `punch_config.py`
* `-v`, `--version_file`: If you name your version file differently you may tell Punch here to load that file instead of `punch_version.py`
* `-p`, `--part`: The name of the part you want to increase to produce the new version. This must be one of the labels listed in the config file and which value is in version file.
* `--verbose`: Verbosely prints information about the execution
* `--version`: Prints the Punch version and project information
* `--init`: Creates each of the `punch_config.py` and `punch_version.py` files if it does not already exist.
* '-s', `--simulate`: Just pretends to increase the version, printing sensible variable values without altering any file.

## The punch workflow

The way punch works can be summarized by the following workflow:

1. The config file and the version file are read from the disk
2. The current version is built according to the configuration of the parts (from the config file) and their actual values (from the version file)
3. The new version is created incrementing the part requested by the user and changing the rest of the version accordingly
4. Each file listed in the configuration file is opened, processed by each of the global or local serializers, replacing the old version with the new one
5. The new version is written into the version file
6. The VCS requested actions are executed

## Configuration

Punch uses two files for its configuration, the _config file_ and the _version file_.

Both have a default value (`punch_config.py` and `punch_version.py` respectively) and both are written in pure Python.

The config file contains the managed files and the version parts description, while the version file contains the actual
values of the version parts.

When you initialize the project using `punch --init` you get the following content for the two files.

### `punch_config.py`
``` python
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = []

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git',
    'commit_message': "Version updated from {{ current_version }} to {{ new_version }}",
}
```

### `punch_version.py`
``` python
major = 0
minor = 1
patch = 0
```

## Version file

The default name of the version file is `punch_version.py`, but this may be changed with the `--version-file` switch.

The version file is a Python valid file that contains a variable declaration for each part of the version described in the config file (see below). **This file will be overwritten by Punch each time it runs**, so avoid inserting here Python code different from the required variables.

An example of the content of this file for a `major.minor.patch` version is 

``` python
major = 2
minor = 4
patch = 12
```

## Config file

The default name of the config file is `punch_config.py`, but this may be changed with the `--config-file` switch.

The config file contains 4 mandatory variables: `__config_version__`, `GLOBALS`, `FILES`, and `VERSION`. The `__config_file__` variable
shall always be equal to `1` and provides a way to introduce later new versions of the configuration file without breaking the
backward compatibility.

The optional variables are: `VCS`.

This file contains pure Pyhton, so feel free to fill it with the Python code you need. Punch is only interested in the value of the variables described here.

### GLOBALS

This variable is a **dictionary** containing variables that are globally valid during the whole execution of punch, if not overridden
by local variables (see `FILES`, for example).

* `serializer` can be a single string o a list of strings, and represents the templates used to search and replace the old version. Each string in `serializer` (or the single one if it is a string) is a [Jinja2](http://jinja.pocoo.org/) template which is rendered with the current version and the new version to get the search and replace patterns.

#### GLOBALS example 1

Let's assume that the current version is `major = 1`, `minor = 4`, and `patch = 6`, and that we increment the `patch` version part. With this configuration

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
}
```

the search pattern becomes `1.4.6` and the replacement pattern is `1.4.7`.

#### GLOBALS example 2

Let's assume that the current version is `major = 1`, `minor = 4`, `patch = 6`, `build = 1`, and that we increment the `patch` version part. Let's assume the `build` part is configured to start with the number `1` instead of `0`. With this configuration

``` python
GLOBALS = {
    'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '+%s' % build }}"
}
```

the search pattern becomes `1.4.6+1` and the replacement pattern is `1.4.7+1`.

#### GLOBALS example 3

Let's assume that the current version is `major = 1`, `minor = 4`, `patch = 6`, `build = 1`, and that we increment the `patch` version part. Let's assume this time the `build` part is configured with a standard integer value. With this configuration

``` python
GLOBALS = {
    'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '+%s' % build if build}}"
}
```

the search pattern becomes `1.4.6+1` and the replacement pattern is `1.4.7`.

#### GLOBALS example 4

Let's assume that the current version is `major = 1`, `minor = 4`, `patch = 6`, and that we increment the `patch` version part. With this configuration

``` python
GLOBALS = {
    'serializer': [
        'Full version: {{ major }}.{{ minor }}.{{ patch }}',
        'Short version: {{ major }}.{{ minor }}'
     ]
}
```

the first search pattern becomes `Full version: 1.4.6` and its replacement pattern is `Full version: 1.4.7`. The second search pattern will be `Short version: 1.4` and the replacement pattern will not change. This may be useful if you have different representation of the same version in a file, or if you want to specifically target uses of that version.


#### Other global variables

You may define any variable in the GLOBALS dictionary and use it later where a Jinja2 temple is available, for example in the `commit_message` of the `VCS` variable.

For example

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}',
    'myvar': 'A personal value'
}

VCS = {
    'name': 'git',
    'commit_message': "Version {{ new_version }} - {{ myvar }}"
}
```

### FILES

This variable is a **list** of files that shall be processed by punch. The simplest entry in this list is a string with a file name, which processes the file using the variables specified in the `GLOBALS` section.

``` python
FILES = ['version.txt', 'mypkg/__init__.py']
```

Each file may also be specified through a **dictionary**. The only mandatory key is `path`, which contains the file path relative to the Punch execution directory (usually the project parent directory). You may also specify here any variable allowed in the `GLOBALS` section, which will be overridden for the current file only.

Example:

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
}

FILES = [
    'version.txt',
    {
        'path': 'mypkg/__init__.py',
        'serializer': '{{ major }}.{{ minor }}'
    }
]
```

In this case the `mypkg/__init__.py` file will be processed using the `{{ major }}.{{ minor }}` serializer instead of `{{ major }}.{{ minor }}.{{ patch }}`. As happens for the `GLOBALS` variable, the serializer of a specific file may also contain a list of string templates instead of a single one.

The local serializers may incorporate specific variables from `GLOBALS`, using the `{{ GLOBALS.<variable> }}` pattern. For example this configuration

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
}

FILES = [
    'version.txt',
    {
        'path': 'mypkg/__init__.py',
        'serializer': '__version__ = {{ GLOBALS.serializer }}'
    }
]
```

sets the local serializer to `__version__ = {{ major }}.{{ minor }}.{{ patch }}` without duplication of the global serializer value.

### VERSION

This variable is a **list** of version parts, in the right hierarchical order. A version part may be just a name, in which case punch build a part made by an integer value starting from `0`.

```python
VERSION = ['major', 'minor', 'patch']
```

This is a description that fits a standard 3-numbers version as described by the plain semver (http://semver.org) without meta information. The order of the parts is important, since when increasing the value of a part (which is what punch does), the following ones shall be reset to their initial value.

Each version part may also be fully specified through a dictionary that contains a `name`, a `type` and other keywords that depend on the part type. The former example may be fully rewritten as

```python
VERSION = [
    {
        'name': 'major',
        'type': 'integer',
        'start_value': 0
    },
    {
        'name': 'minor',
        'type': 'integer',
        'start_value': 0
    },
    {
        'name': 'patch',
        'type': 'integer',
        'start_value': 0
    }
]
```

The following list describes the different types of parts you may use and their custom options.

* `integer`: a positive integer value
    * `start_value`: [default: `0`] The starting value for this part.

* `value_list`: a list of values. When incrementing the last value the field goes back to the first.
    * `allowed_values`: [mandatory] The list of allowed values for this field (e.g. `['alpha`, `beta`])


### VCS

Punch can be configured to automatically commit the version change to one of the supported VCS. The VCS
variable in the config file, if present, enables this feature. The format of the variable is that of a
dictionary encompassing the 'name' variable with the name of the VCS of choice. Currently supported VCSs are

* 'git'
* 'git-flow'

The `VCS` variable is a **dictionary** which must contain the `'name'` key with the name of the adapter of choice (available values are listed above).
 
This dictionary is processed using Jinja2 and with a dictionary of variables that contains all global variables and the following sepcial variables:
 
 * `current_version`: is the serialized value of the current version. In case of multiple serializers the first one is used.
 * `new_version`: is the serialized value of the new version. In case of multiple serializers the first one is used.

Other keys accepted by the `VCS` dictionary are

* `commit_message`: a Jinja2 template with the message used to commit the version advancement. (default: `"Version updated {{ current_version }} -> {{ new_version }}"`
* `finish_release`: a boolean which tells the VCS to commit the changes. (default: `True`)
* `options`: a **dictionary** of VCS-specific options (see the relevant section below)

#### git

The `git` VCS adapter provides support for project managed through Git. The adapter automatically commits the version advancement and tags the resulting repository status.
 
The options supported by this adapter are:

* `'make_release_branch'`: creates a dedicated release branch to commit the version advancement, then merges it into master. (default: `True`)
* `'annotate_tags` and `'annotation_message'`: tags the repository status after committing the release update with an annotated tag and the given annotation message. (defaults: `False` and `"Version {{ new_version }}"`)
* `'tag'`: the name of the tag (default: the value of the `new_version` variable)

#### git-flow

The `git-flow` VCS adapter follows the well-known git-flow workflow, so the release is done starting from the `develop` branch, with a dedicated release branch. There are currently no options for this adapter.

## Contributing

See the CONTRIBUTING file for detailed information. Please remember that this project is actively developed in the `develop` branch, so be sure to work there if you try to implement new feature of fix bugs.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.

This project has been heavily inspired by [bumpversion](https://github.com/peritus/bumpversion), and I want to thank [Filip Noetzel](https://github.com/peritus), the author of that project for his work and the inspiring ideas.

