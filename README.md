# Punch

[![Build Status](https://travis-ci.org/lgiordani/punch.svg?branch=master)](https://travis-ci.org/lgiordani/punch)
[![Version](https://img.shields.io/pypi/v/punch.py.svg)](https://github.com/lgiordani/punch)

Update your version while having a drink

## About punch

Punch is a configurable version updater, and you can use to automate the management of your project's version number.

Punch stores the version of your project in its own file. Each time you need to update it, Punch runs through the configured
 files and replaces the old version with the new one. Additionally, Punch may also automatically commit the version change
 on your VCS of choice.

This project has been heavily inspired by [bumpversion](https://github.com/peritus/bumpversion), and I want to thank Filip Noetzel, the author of that project for his work and the inspiring ideas.

## Installation

Punch is available for both Python 2 and Python 3 through pip. Just create a virtual environment and run

``` sh
pip install punch.py
```

To start working with Punch you need a configuration file and a version file. You may ask Punch to create the two files for you with
 reasonable starting values with the flag `--init`
 
``` sh
punch --init
```

which will create the `punch_config.py` and `punch_version.py` files in the current directory.

## Contributing

See the CONTRIBUTING file for detailed information. Please remember that this project is actively developed in the `develop` branch, so be sure to work there if you try to implement new feature of fix bugs.