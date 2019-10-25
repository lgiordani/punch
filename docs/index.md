# Punch

[![Build Status](https://travis-ci.org/lgiordani/punch.svg?branch=master)](https://travis-ci.org/lgiordani/punch)
[![Version](https://img.shields.io/pypi/v/punch.py.svg)](https://github.com/lgiordani/punch)

Update your version while having a drink

## About punch

Punch is a configurable version updater, and you can use to automate the management of your project's version number.

Punch stores the version of your project in its own file. Each time you need to update it, Punch runs through the configured files and replaces the old version with the new one. Additionally, Punch may also automatically commit the version change on your VCS of choice.

## Installation

Punch is available for both Python 2 and Python 3 through pip. Just create a virtual environment and run

``` sh
pip install punch.py
```

To start working with Punch you need a configuration file and a version file. You may ask Punch to create the two files for you with reasonable starting values with the flag `--init`

``` sh
punch --init
```

which will create the `punch_config.py` and `punch_version.py` files in the current directory. These names are used by default by Punch, but you may change them (see later).

## Command line options

Punch may be invoked with the following command line options

* `-c`, `--config_file`: If you name your config file differently you may tell Punch here to load that file instead of `punch_config.py`.
* `-v`, `--version_file`: If you name your version file differently you may tell Punch here to load that file instead of `punch_version.py`.
* `-p`, `--part`: The name of the part you want to increase to produce the new version. This must be one of the labels listed in the config file and which value is in version file.
* `--set-part`: A comma-separated list of "{part}={value}" tokens. The new version parts will be set accordingly. This will not reset the following parts.
* `--reset-on-set`: Resets the following parts after setting a part to a specific value. You may not set more than a part if you use this flag.
* `--verbose`: Verbosely prints information about the execution.
* `--version`: Prints the Punch version and project information.
* `--init`: Creates each of the `punch_config.py` and `punch_version.py` files if it does not already exist.
* `-s`, `--simulate`: Just pretends to increase the version, printing sensible variable values without altering any file (implies --verbose).

## Usage examples

### Init

Create the two `punch_config.py` and `punch_version.py` files if they are not existing.

`punch --init`

### Standard invocation

Increase the `minor` part and reset the following ones (e.g. `1.0.0 --> 1.1.0`)

`punch --part minor`

### Explicitly set a part

Sets the `minor` part to `23` and leave the following parts untouched (e.g. `1.2.3 --> 1.23.3`)

`punch --set-part minor=23`

### Increment version and set a part

Increase the `major` part, then reset the following ones. Finally set the `minor` part to `23` leaving the following parts untouched (e.g. `1.2.3 (--> 2.0.0) --> 2.23.0`)

`punch --part major --set-part minor=23`

### Explicitly set and reset

Set the `minor` part to `23` and reset the following parts (e.g. `1.2.3 --> 1.23.0`)

`punch --set-part minor=23 --reset-on-set`

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

The config file contains 4 mandatory variables: `__config_version__`, `GLOBALS`, `FILES`, and `VERSION`. The `__config_version__` variable shall always be equal to `1` and provides a way to introduce later new versions of the configuration file without breaking the backward compatibility.

The optional variables are: `VCS`.

This file contains pure Pyhton, so feel free to fill it with the Python code you need. Punch is only interested in the value of the variables described here.

### GLOBALS

This variable is a **dictionary** containing variables that are globally valid during the whole execution of punch, if not overridden
by local variables (see `FILES`, for example).

* `serializer` represents the templates used to search and replace the old version. This can be **string**, a **list of strings** or a **dictionary**. Each serializer is a [Jinja2](http://jinja.pocoo.org/) template which is rendered with the current version and the new version to get the search and replace patterns. Expressing serializer with a dictionary allows you to give them a name and to refer to them in other parts of punch. for example when using a VCS.

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


#### GLOBALS example 5

The previous configuration can be expressed with named serializers.

``` python
GLOBALS = {
    'serializer': {
        'full': 'Full version: {{ major }}.{{ minor }}.{{ patch }}',
        'short': 'Short version: {{ major }}.{{ minor }}'
     }
}
```

This allows you to refer to the serializers in other parts of punch with a specific name.


#### Other global variables

You may define any variable in the GLOBALS dictionary and use it later where a Jinja2 template is available, for example in the `commit_message` of the `VCS` variable.

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

This variable is a **list** of version parts, in the right hierarchical order. A version part may be just a name, in which case punch builds a part made by an integer value starting from `0`.

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
    - `start_value`: [default: `0`] The starting value for this part.
* `value_list`: a list of values. When incrementing the last value the field goes back to the first.
    - `allowed_values`: [mandatory] The list of allowed values for this field (e.g. `['alpha`, `beta`])
* `date`: part of the current date (aka `datetime.now()`). When incrementing the current date is always used.
    - `fmt`: [mandatory] The formatted date string. This uses the Python `strftime()` function, so any string can contain the directives accepted by this function (see [this reference](http://strftime.org/) or [the official docuemntation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)). Also, some shortcuts from the [CalVer](http://calver.org/) versioning convention have been introduced. The description can be found [here](http://calver.org/#scheme). If `fmt` is just one of those punch will provide the correct value, but those shortcuts cannot be used in a more complex string.

### VCS

Punch can be configured to automatically commit the version change to one of the supported VCS. The VCS
variable in the config file, if present, enables this feature. The format of the variable is that of a
dictionary encompassing the 'name' variable with the name of the VCS of choice. Currently supported VCSs are

* 'git'
* 'git-flow'
* 'hg' (Mercurial)

The `VCS` variable is a **dictionary** which must contain the `'name'` key with the name of the adapter of choice (available values are listed above).

This dictionary is processed using Jinja2 and with a dictionary of variables that contains all global variables and the following sepcial variables:

 * `current_version`: is the serialized value of the current version.
 * `new_version`: is the serialized value of the new version.

If multiple serializers are provided in a list, the first one is used to create the versions for the VCS. If serializers are provided as a dictionary, you need to specify the `VCS_SERIALIZER` top level config variable, with the name of the chosen serializer.

Other keys accepted by the `VCS` dictionary are

* `commit_message`: a Jinja2 template with the message used to commit the version advancement. (default: `"Version updated {{ current_version }} -> {{ new_version }}"`
* `finish_release`: a boolean which tells the VCS to commit the changes. (default: `True`)
* `options`: a **dictionary** of VCS-specific options (see the relevant section below)
* `include_files`: a list of files to include in the commit (see the relevant section below)
* `include_all_files`: a boolean flag that when se includes all untracked files in the commit (see the relevant section below)

#### git

The `git` VCS adapter provides support for project managed through Git. The adapter automatically commits the version advancement and tags the resulting repository status.

The options supported by this adapter are:

* `'target_branch'`: the release will be merged into this branch. (default: `'master'`)
* `'make_release_branch'`: creates a dedicated release branch to commit the version advancement, then merges it into the target branch. (default: `True`)
* `'annotate_tags` and `'annotation_message'`: tags the repository status after committing the release update with an annotated tag and the given annotation message. (defaults: `False` and `"Version {{ new_version }}"`)
* `'tag'`: the name of the tag (default: the value of the `new_version` variable)

#### git-flow

The `git-flow` VCS adapter follows the well-known git-flow workflow, so the release is done starting from the `develop` branch, with a dedicated release branch. There are currently no options for this adapter.

#### hg

The 'hg' VCS adapter provides support for projects managed with Mercurial. The options suported by this adapter are:

* `'branch'`: the name of the newly created branch (default: `default`)

#### Include files

By default punch adds in a commit its config file, its version file, and all the files listed in the `FILES` variable of the config file. If you need to add other files that you plan to change manually outside of the punch workflow you can specify them with the `include_files` key of the `VCS` dictionary. For example

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["version.txt"]

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git',
    'include_files': ['HISTORY.rst']
}
```

manages the version contained in the file `version.txt`, but tries to add in the commit the file `HISTORY.rst` as well.

If you want to configure punch to include automatically all the untracked files in the commit you can set the `include_all_files` flag to `True`

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["version.txt"]

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git',
    'include_all_files': True
}
```

### Actions

Sometimes complex workflows are required, especially when `date` parts are involved. Those fields come from an external source (the system clock), and their updated status is thus generally speaking unpredictable. You can obviously say at each execution if the field will be updated or not, but the link between the command line options and the updates performed by Punch is in general not evident.

Consider a configuration like the following

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': '{{year}}.{{build}}',
}

FILES = ["README.md"]

VERSION = [
    {
        'name': 'year',
        'type': 'date',
        'fmt': '%Y'
    },
    'build'
]
```

This captures a situation where `build`, which is hierarchically lower than `year`, is reset when `year` changes. During the year the command issued by the user is `punch --part build`, which updates `build` and leaves `year` untouched. On the 1st of January of the new year, however, the command has to be `punch --part year`, otherwise the `year` part doesn't get modifed, and `part` doesn't get reset. Issuing the last command at every build doesn't give the expected result, as `year` doesn't change, and `build` is not incremented.

As mentioned before, this happens because date version parts are updated from an external source, which is unpredictable.

Punch allows then to define actions, that is specific workflows that cannot be captured by the standard syntax. The only possible action type at the moment is `conditional_reset`.

Actions are defined by an `ACTIONS` list in the config file, with the following syntax

``` python
ACTIONS = {
    'action_name': {
        'type': 'action_type',
        # ...
    }
}
```

where `action_name` is a free name that represents the action in your specific setup and `action_type` can only be `conditional_reset` at the moment. The dictionary can contain other keys required or supported by the specific action type.

#### Conditional reset action

``` python
ACTIONS = {
    'mbuild': {
        'type': 'conditional_reset',
        'field': 'build',
        'update_fields': ['year', 'month']
    }
}
```

The conditional reset action workflow is the following.

1. Update all the fields listed in `update_fields`.
2. If the full version changed then reset `field`, otherwise just increment it.

So for the above configuration if the current version is `2017.01-4` on 31 January 2017 the command `punch --action mbuild` creates version `2017.01-5` (`year` and `month` do not change, so `build` is incremented), while on the 01 February 2017 it will create version `2017.02-0` (`build` is reset.

## Examples

The following are examples of Punch configuration that show the different options implemented in it. The configuration files are all implemented in working tests that you can find in the `test_config_*.py` files of the test suite.

### Plain SemVer

This is an example configuration that uses SemVer (http://semver.org) without any metadata (as described by parts 9 and 10 of the specification).

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}'
}

FILES = []

VERSION = ['major', 'minor', 'patch']
```

| Part updated  | Current version | New version |
| ------------- |:---------------:|:-----------:|
| major         | 1.0.0           | 2.0.0       |
| minor         | 1.0.0           | 1.1.0       |
| patch         | 1.0.0           | 1.0.1       |

### CalVer Ubuntu-style

This example uses a versioning style taken from Ubuntu, which uses the CalVer 'YY.MM' syntax, that is the current year and the current month without zero-padding. See [here](http://calver.org/#ubuntu) for the CalVer explanation.

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': '{{year}}.{{month}}',
}

FILES = ["README.md"]

VERSION = [
    {
        'name': 'year',
        'type': 'date',
        'fmt': 'YY'
    },
    {
        'name': 'month',
        'type': 'date',
        'fmt': 'MM'
    }
]
```

| Part updated  | Current version | New version |
| ------------- |:---------------:|:-----------:|
| year          | 2016            | current(1)  |
| month         | 10              | current(2)  |

(1) uses the current unpadded year, like `4` if the current year is 2004, `17` is the current year is 2017, and so on.

(2) uses the current unpadded month, so one of the values in the list `[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]`

### SemVer with build metadata

This configuration implements SemVer with build metadata (as described by part 10 of the specification). This build number is made of three digit and starts with 1

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '+{0:03d}'.format(build) }}"
}

FILES = ["README.md"]

VERSION = [
            'major',
            'minor',
            'patch',
            {
                'name': 'build',
                'type': 'integer',
                'start_value': 1
            }
          ]
```

| Part updated  | Current version | New version |
| ------------- |:---------------:|:-----------:|
| major         | 1.0.0+001       | 2.0.0+001   |
| minor         | 1.0.0+001       | 1.1.0+001   |
| patch         | 1.0.0+001       | 1.0.1+001   |
| build         | 1.0.0+001       | 1.0.0+002   |

### SemVer with prerelease metadata

This configuration implements SemVer with prerelease metadata (as described by part 9 of the specification). The chosen prerelease strings are `'alpha'` and `'beta`.

WARNING: This use of the prerelease parts is pretty incomplete and a bit useless. It will be soon updated

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '-{}'.format(prerelease) if prerelease }}"
}

FILES = ["README.md"]

VERSION = [
            'major',
            'minor',
            'patch',
            {
                'name': 'prerelease',
                'type': 'value_list',
                'allowed_values': ['', 'alpha', 'beta']
            }
          ]
```


| Part updated  | Current version | New version |
| ------------- |:---------------:|:-----------:|
| major         | 1.0.0-alpha     | 2.0.0       |
| minor         | 1.0.0-alpha     | 1.1.0       |
| patch         | 1.0.0-alpha     | 1.0.1       |
| prerelease    | 1.0.0-alpha     | 1.0.0-beta  |
| prerelease    | 1.0.0-beta      | 1.0.0       |

When using tags like the prerelease shown here you may take advantage of the `--set-part` option that allows to explicitly set the value of a version part when creating the new version.

If you put the empty string as last element of the string you get the following behaviour

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '-{}'.format(prerelease) if prerelease }}"
}

FILES = ["README.md"]

VERSION = [
            'major',
            'minor',
            'patch',
            {
                'name': 'prerelease',
                'type': 'value_list',
                'allowed_values': ['alpha', 'beta', '']
            }
          ]
```


| Part updated  | Current version | New version |
| ------------- |:---------------:|:-----------:|
| major         | 1.0.0-alpha     | 2.0.0-alpha |
| minor         | 1.0.0-alpha     | 1.1.0-alpha |
| patch         | 1.0.0-alpha     | 1.0.1-alpha |
| prerelease    | 1.0.0-alpha     | 1.0.0-beta  |
| prerelease    | 1.0.0-beta      | 1.0.0       |


## Contributing

See the CONTRIBUTING file for detailed information. Please remember that this project is actively developed in the `develop` branch, so be sure to work there if you try to implement new feature of fix bugs.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.

This project has been heavily inspired by [bumpversion](https://github.com/peritus/bumpversion), and I want to thank [Filip Noetzel](https://github.com/peritus), the author of that project for his work and the inspiring ideas.

Mercurial support thanks to [Michele d'Amico](https://github.com/la10736).
