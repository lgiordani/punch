# Punch

[![Build Status](https://travis-ci.org/lgiordani/punch.svg?branch=master)](https://travis-ci.org/lgiordani/punch)
[![Version](https://img.shields.io/pypi/v/punch.py.svg)](https://github.com/lgiordani/punch)

Update your version while having a drink

## About punch

Punch is a configurable version updater, and you can use to automate the management of your project's version number.

Punch stores the version of your project in its own file. Each time you need to update it, Punch runs through the configured files and replaces the old version with the new one. Additionally, Punch may also automatically commit the version change on your VCS of choice.

Punch has configurable actions (although they are still in an initial state of development), multiple serializers, and can scan the release notes to check for missing entries. It supports Git, Git Flow and Mercurial.

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
* `-a`: 
* `--action-options`: 
* `--action-flags`: 
* `--reset-on-set`: Resets the following parts after setting a part to a specific value. You may not set more than a part if you use this flag.
* `-q`: 
* `--verbose`: Verbosely prints information about the execution.
* `--version`: Prints the Punch version and project information.
* `--init`: Creates each of the `punch_config.py` and `punch_version.py` files if it does not already exist.
* `-s`, `--simulate`: Just pretends to increase the version, printing sensible variable values without altering any file (implies --verbose).

## Contributing

See the CONTRIBUTING file for detailed information. Please remember that this project is actively developed in the `develop` branch, so be sure to work there if you try to implement new feature of fix bugs.

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [`audreyr/cookiecutter-pypackage`](https://github.com/audreyr/cookiecutter-pypackage) project template.

This project has been heavily inspired by [bumpversion](https://github.com/peritus/bumpversion), and I want to thank [Filip Noetzel](https://github.com/peritus), the author of that project for his work and the inspiring ideas.

Mercurial support thanks to [Michele d'Amico](https://github.com/la10736).
