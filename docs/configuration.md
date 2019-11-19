# Configuration

Punch uses two files for its configuration, the _config file_ and the _version file_.

Both have a default value (`punch_config.py` and `punch_version.py` respectively) and both are written in pure Python.

The config file contains the managed files and the version parts description, while the version file contains the actual values of the version parts. When you initialize the project using `punch --init` you get the following content for `punch_config.py`

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

And the following content for `punch_version.py`

``` python
major = 0
minor = 1
patch = 0
```

## Version file

The default name of the version file is `punch_version.py`, but this may be changed with the `--version-file` switch.

The version file is a Python valid file that contains a variable declaration for each part of the version described in the config file (see below). **This file will be overwritten by Punch each time it runs**, so never edit its content, as any change will be lost.

An example of the content of this file for a `major.minor.patch` version is

``` python
major = 2
minor = 4
patch = 12
```

## Config file

The default name of the config file is `punch_config.py`, but this may be changed with the `--config-file` switch.

The config file contains 4 mandatory variables:

* `__config_version__`
* `GLOBALS`
* `FILES`
* `VERSION`

The `__config_version__` variable at the moment can only assume the value `1`. It provides a way to introduce later new versions of the configuration file without breaking the backward compatibility.

The optional variables are:

* `VCS`

This file contains pure Python, so if you need to create some of its content programmatically feel free to do it. Punch uses only the value of the variables described here, any other code will be executed but will not affect the configuration.

*A note on security*: configuration files that can contain code which is executed by the application are a very bad idea for servers, as they provide a potential way for attackers to execute code with a different privilege level. Punch is however a tool that developers use to work on their own project, and whoever can edit the configuration can already execute all the actions that Punch performs. This means that there is no threat in having a configuration file that contains code for Punch.

## Serializers

Serializers are the templates used to search and replace the old version with the new one. They are filled with the values of the current version and the result is used by Punch to scan the controlled files. Whenever a match is found, Punch replaces it with the same template filled with the values of the new version.

So for example, Given a current version of 1.2.3 and a new version of 1.3.0, a serializer like `'version {{ major }}.{{ minor }}.{{ patch }}'` makes Punch search for the string `'version 1.2.3'` and replace it with `'version 1.3.0'`.

Serializers can be found in different parts of the configuration file, but all share the same syntax. They can be

* A **string** containing a single serializer, e.g. `'{{ major }}.{{ minor }}.{{ patch }}'`
* A **list of strings**, each string being a serializer, e.g. `['{{ major }}.{{ minor }}.{{ patch }}', '{{ major }}.{{ minor }}']`
* A **dictionary**, each entry being a serializer, e.g.
```
{
    'full': '{{ major }}.{{ minor }}.{{ patch }}',
    'short': '{{ major }}.{{ minor }}'
}
```


The dictionary form is called "named serializer", and the one shown here is its shorter form. A longer form of the named serializers is described in the Advanced configuration section. The reason behind named serializers is that this way you can choose which serializer you want to use for certain tasks (see the documentation of the `VCS_SERIALIZER` configuration option).

Serializers are Jinja2 templates so you can access all the template functions that the engine provides.

### Example 1

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
}
```

The current version is

```
major = 1
minor = 4
patch = 6
```

When we increment the `patch` version part, the search pattern for the old version becomes `1.4.6` and the replacement string will be `1.4.7`.

### Example 2

``` python
GLOBALS = {
    'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '+%s' % build }}"
}
```

The current version is

```
major = 1
minor = 4
patch = 6
build = 1
```

and the `build` part is configured to start with the number `1` instead of `0` (see `Actions`).

When we increment the `patch` version part, the search pattern for the old version becomes `1.4.6+1` and the replacement string will be `1.4.7+1`.

### Example 3

``` python
GLOBALS = {
    'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '+%s' % build if build }}"
}
```

The current version is

```
major = 1
minor = 4
patch = 6
build = 1
```

and the `build` part is configured with a standard integer value. 

When we increment the `patch` version part, the search pattern for the old version becomes `1.4.6+1` and the replacement string will be `1.4.7`.

### Example 4

``` python
GLOBALS = {
    'serializer': [
        'Full version: {{ major }}.{{ minor }}.{{ patch }}',
        'Short version: {{ major }}.{{ minor }}'
     ]
}
```

The current version is

```
major = 1
minor = 4
patch = 6
```

When we increment the `patch` version part, the first search pattern becomes `Full version: 1.4.6` and its replacement pattern is `Full version: 1.4.7`. The second search pattern will be `Short version: 1.4` and the replacement pattern will be the same. This is useful if you have different representation of the version in the project.

### Example 5

``` python
GLOBALS = {
    'serializer': {
        'full': 'Full version: {{ major }}.{{ minor }}.{{ patch }}',
        'short': 'Short version: {{ major }}.{{ minor }}'
     }
}
```

This is the same configuration shown in the previous example, but it uses named serializers. This allows you to refer to the serializers with a specific name in other parts of the Punch configuration file.

## GLOBALS

This variable is a **dictionary** containing variables that are globally valid during the whole execution of Punch, if not overridden by local variables (see `FILES`, for example).

* `serializer` is the set of serializers declared globally (see the section about Serializers).

Custom variables can be defined adding their name and value, and reused in other parts of the configuration file.

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

## FILES

This variable is a **list** of files that will be processed by Punch using the variables specified in the `GLOBALS` section.

The simplest way to add a file is to add a **string** with its name

``` python
FILES = ['version.txt', 'mypkg/__init__.py']
```

A file may also be specified through a **dictionary**. The only mandatory key is `path`, which contains the file path relative to the Punch execution directory (usually the project parent directory). This format allows you to override any variable included in the `GLOBALS` section for the current file only.

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

In this example the `mypkg/__init__.py` file will be processed using the `{{ major }}.{{ minor }}` serializer instead of `{{ major }}.{{ minor }}.{{ patch }}`. As happens for the `GLOBALS` variable, the serializer of a specific file may also contain a list of string templates instead of a single one, or named serializers in a dictionary.

The local serializers may incorporate specific variables from `GLOBALS`, using the `{{ GLOBALS.<variable> }}` pattern. For example the configuration

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

## VERSION

This variable is a **list** of version parts, in hierarchical order. A version part may be just a name, in which case Punch builds a part made by an integer value starting from `0`.

```python
VERSION = ['major', 'minor', 'patch']
```

This is a description that fits a standard 3-numbers version as described by the plain semver (http://semver.org) without meta information. The order of the parts is important, since when increasing the value of a part (which is what Punch does), the following ones shall be reset to their initial value.

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

The following list describes the different types of parts that you can use and their custom options.

* `integer`: a positive integer value like `1`, `2`, `3` and so on.
    - `start_value`: [default: `0`] The starting value for this part.
* `value_list`: a list of custom values. The list is wrapped, so when incrementing the last value the field goes back to the first one.
    - `allowed_values`: [mandatory] The list of allowed values for this field (e.g. `['alpha', 'beta']`, `['A', 'B', 'C']`)
* `date`: part of the current date given by `datetime.now()`. When incrementing this part, the current date is always used.
    - `fmt`: [mandatory] The formatted date string. This uses the Python `strftime()` function, so any string can contain the directives accepted by this function (see [this reference](http://strftime.org/) or [the official docuemntation](https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior)). Also, some shortcuts from the [CalVer](http://calver.org/) versioning convention have been introduced. The description can be found [here](http://calver.org/#scheme). If `fmt` is just one of those Punch will provide the correct value, but those shortcuts cannot be used in a more complex string.

## VCS

Punch can be configured to automatically commit the version change to one of the supported VCS. The VCS
variable in the configuration file, if present, enables this feature. The `VCS` variable is a **dictionary** which must contain the `'name'` key with the name of the adapter of choice. Currently supported VCSs are

* Git (`'name': 'git'`)
* Git with git-flow (`'name': 'git-flow'`)
* Mercurial (`'name': 'hg'`)

Example:

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["version.txt"]

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git',
}
```

The `VCS` dictionary can contain other keys shared by all VCSs, and some keys that are specific for each system. All values in the dictionary are all treated as Jinja2 templates. When rendering them, Punch uses all global variables (see `GLOBALS` and the following special variables:

 * `current_version`: is the serialized value of the current version.
 * `new_version`: is the serialized value of the new version.

If multiple serializers are provided by the `serializer` global option, the first one is used to create the versions for the VCS. If serializers are provided as a dictionary, you need to specify the `VCS_SERIALIZER` top level configuration variable, with the name of the chosen serializer.

Example:

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': {
        'full': '{{major}}.{{minor}}.{{patch}}',
        'short': '{{major}}.{{minor}}'
    }
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']

VCS_SERIALIZER = 'full'

VCS = {
    'name': 'git'
}
```

Other keys accepted by the `VCS` dictionary are

* `commit_message`: a Jinja2 template with the message used to commit the version advancement. (default: `"Version updated {{ current_version }} -> {{ new_version }}"`
* `finish_release`: a boolean which tells the VCS to commit the changes. (default: `True`)
* `options`: a **dictionary** of VCS-specific options (see the relevant section below)
* `include_files`: a list of files to include in the commit (see the relevant section below)
* `include_all_files`: a boolean flag that when se includes all untracked files in the commit (see the relevant section below)

### Git

The `git` VCS adapter provides support for project managed through Git. The adapter automatically commits the version advancement and tags the resulting repository status.

The options supported by this adapter are:

* `'target_branch'`: the release will be merged into this branch. (default: `'master'`)
* `'make_release_branch'`: flag that creates a dedicated release branch to commit the version advancement, then merges it into the target branch. (default: `True`)
* `'annotate_tags`: flag that tags the repository status after committing the release update with an annotated tag (default: `False`)
* `'annotation_message'`: the message used for the annotated tag (default: `"Version {{ new_version }}"`)
* `'tag'`: the name of the tag (default: the value of the `new_version` variable)

### Git Flow

The `git-flow` VCS adapter follows the well-known git-flow work flow, so the release is done starting from the `develop` branch, with a dedicated release branch. There are currently no options for this adapter.

### hg

The 'hg' VCS adapter provides support for projects managed with Mercurial. The options supported by this adapter are:

* `'branch'`: the name of the newly created branch (default: `default`)

### Include files

By default Punch adds in a commit its own configuration file, its version file, and all the files listed in the `FILES` variable of the configuration file. If you need to add other files that you plan to change manually outside of the Punch work flow you can specify them with the `include_files` key of the `VCS` dictionary. For example

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

manages the version contained in the file `version.txt`, but adds in the commit the file `HISTORY.rst` as well.

If you want to configure Punch to include automatically all the untracked files in the commit you can set the `include_all_files` flag to `True`

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

