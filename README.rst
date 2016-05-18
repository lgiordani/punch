Punch
=====

Update your version while having a drink

|Build Status| |Version|

Update your version while having a drink

-  Documentation: https://punch.readthedocs.org.

This project has been heavily inspired by bumpversion, and I want to
thank Filip Noetzel, the author of that project for his work and the
inspiring ideas.

The punch workflow
------------------

The way punch works can be summarized by the following workflow:

-  The config file and the version file are read from the disk
-  The current version is built according to the configuration of the
   parts and their actual values
-  The new version is created incrementing the part requested by the
   user and changing the rest of the version accordingly
-  Each file listed in the configuration file is opened, processed by
   each of the global or local serializers, replacing the old version
   with the new one
-  The new version is written into the version file
-  The VCS requested actions are executed

Configuration
-------------

Punch uses two files for its configuration, the *config file* and the
*version file*.

Both have a default value (``punch_config.py`` and ``punch_version.py``
respectively) and both are written in pure Python.

The config file contains the managed files and the version parts
description, while the version file contains the actual values of the
version parts.

Version file
~~~~~~~~~~~~

The default name of the version file is ``punch_version.py``, but this
may be changed with the ``--version-file`` switch.

The version file is a Python valid file that contains a variable
declaration for each part of the version described in the config file
(see below). **This file will be overwritten by punch each time it
runs**, so avoid inserting here Python code different from the required
variables.

An example of the content of this file for a ``major.minor.patch``
version is

.. code:: python

    major = 2
    minor = 4
    patch = 12

Config file
~~~~~~~~~~~

The default name of the config file is ``punch_config.py``, but this may
be changed with the ``--config-file`` switch.

The config file contains 4 mandatory variables: ``__config_version__``,
``GLOBALS``, ``FILES``, and ``VERSION``. The ``__config_file__``
variable shall always be equal to ``1`` and provides a way to introduce
later new versions of the configuration file without breaking the
backward compatibility.

The optional variables are: ``VCS``.

This file contains pure Pyhton, so feel free to fill it with the Python
code you need. Punch is only interested in the value of the 4 variables
described here.

GLOBALS
^^^^^^^

This variable is a **dictionary** containing variables that are globally
valid during the whole execution of punch, if not overridden by local
variables (see ``FILES``, for example).

-  ``serializer`` can be a single string o a list of strings, and
   represents the templates used to search and replace the old version.
   Each string in ``serializer`` (or the single one if it is a string)
   is a Jinja2 template which is rendered with the current version and
   the new version to get the search and replace patterns.

Example
'''''''

Let's assume that the current version is ``major = 1``, ``minor = 4``,
and ``patch = 6``, and that we increment the ``patch`` version part.
With this configuration

.. code:: python

    GLOBALS = {
        'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
    }

the search pattern becomes ``1.4.6`` and the replacement pattern is
``1.4.7``.

Example
'''''''

Let's assume that the current version is ``major = 1``, ``minor = 4``,
``patch = 6``, ``build = 1``, and that we increment the ``patch``
version part. Let's assume the ``build`` part is configured to start
with the number ``1`` instead of ``0``. With this configuration

.. code:: python

    GLOBALS = {
        'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '+%s' % build if build}}"
    }

the search pattern becomes ``1.4.6+1`` and the replacement pattern is
``1.4.7+1``.

Example
'''''''

Let's assume that the current version is ``major = 1``, ``minor = 4``,
``patch = 6``, ``build = 1``, and that we increment the ``patch``
version part. Let's assume this time the ``build`` part is configured
with a standard integer value. With this configuration

.. code:: python

    GLOBALS = {
        'serializer': "{{ major }}.{{ minor }}.{{ patch }}{{ '+%s' % build if build}}"
    }

the search pattern becomes ``1.4.6+1`` and the replacement pattern is
``1.4.7``.

Example
'''''''

Let's assume that the current version is ``major = 1``, ``minor = 4``,
``patch = 6``, and that we increment the ``patch`` version part. With
this configuration

.. code:: python

    GLOBALS = {
        'serializer': [
            'Full version: {{ major }}.{{ minor }}.{{ patch }}',
            'Short version: {{ major }}.{{ minor }}'
         ]
    }

the first search pattern becomes ``Full version: 1.4.6`` and its
replacement pattern is ``Full version: 1.4.7``. The second search
pattern will be ``Short version: 1.4`` and the replacement pattern will
not change. This may be useful if you have different representation of
the same version in a file, or if you want to specifically target uses
of that version.

Other global variables
''''''''''''''''''''''

You may define any variable in the GLOBALS dictionary and use it later
where a Jinja2 temple is available, for example in the
``commit_message`` of the ``VCS`` variable.

FILES
^^^^^

This variable is a **list** of files that shall be processed by punch.
The simplest entry in this list is a string with a file name, which
processes the file using the variables specified in the ``GLOBALS``
section.

.. code:: python

    FILES = ['version.txt', `mypkg/__init__.py`]

A file may also be specified through a **dictionary**. The only
mandatory key is ``path``, which contains the file path relative to the
punch execution directory (usually the project parent directory). You
may also specify here any variable allowed in the ``GLOBALS`` section,
which will be overridden for the current file only.

.. code:: python

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

In this case the ``mypkg/__init__.py`` file will be processed using the
``{{ major }}.{{ minor }}`` serializer instead of
``{{ major }}.{{ minor }}.{{ patch }}``. As happens for the ``GLOBALS``
variable, the serializer of a specific file may also contain a list of
string templates instead of a single one.

The local serializers may incorporate specific variables from
``GLOBALS``, using the ``{{ GLOBALS.<variable> }}`` pattern. For example
this configuration

.. code:: python

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

sets the local serializer to
``__version__ = {{ major }}.{{ minor }}.{{ patch }}`` without
duplication of the global serializer value.

VERSION
^^^^^^^

This variable is a **list** of version parts, in the right hierarchical
order. A version part may be just a name, in which case punch build a
part made by an integer value starting from ``0``.

.. code:: python

    VERSION = ['major', 'minor', 'patch']

This is a description that fits a standard 3-numbers version as
described by the plain semver (http://semver.org) without meta
information. The order of the parts is important, since when increasing
the value of a part (which is what punch does), the following ones shall
be reset to their initial value.

Each version part may also be fully specified through a dictionary that
contains a ``name``, a ``type`` and other keywords that depend on the
part type. The former example may be fully rewritten as

.. code:: python

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

The following list describes the different types of parts you may use
and their custom options.

-  ``integer``: a positive integer value

   -  ``start_value``: [default: ``0``] The starting value for this
      part.

-  ``value_list``: a list of values. When incrementing the last value
   the field goes back to the first.

   -  ``allowed_values``: [mandatory] The list of allowed values for
      this field (e.g. ``['alpha``, ``beta``])

VCS
^^^

Punch can be configured to automatically commit the version change to
one of the supported VCS. The VCS variable in the config file, if
present, enables this feature. The format of the variable is that of a
dictionary encompassing the 'name' variable with the name of the VCS of
choice. Currently supported VCSs are

-  'git'
-  'git-flow'

The ``VCS`` variable is a **dictionary** which must contain the
``'name'`` key with the name of the adapter of choice (available values
are listed above).

This dictionary is processed using Jinja2 and with a dictionary of
variables that contains all global variables and the following sepcial
variables:

-  ``current_version``: is the serialized value of the current version.
   In case of multiple serializers the first one is used.
-  ``new_version``: is the serialized value of the new version. In case
   of multiple serializers the first one is used.

Other keys accepted by the ``VCS`` dictionary are

-  ``commit_message``: a Jinja2 template with the message used to commit
   the version advancement. (default:
   ``"Version updated {{ current_version }} -> {{ new_version }}"``
-  ``finish_release``: a boolean which tells the VCS to commit the
   changes. (default: ``True``)
-  ``options``: a **dictionary** of VCS-specific options (see the
   relevant section below)

git
'''

The ``git`` VCS adapter provides support for project managed through
Git. The adapter automatically commits the version advancement and tags
the resulting repository status.

The options supported by this adapter are:

-  ``'make_release_branch'``: creates a dedicated release branch to
   commit the version advancement, then merges it into master. (default:
   ``True``)
-  ``'annotate_tags`` and ``'annotation_message'``: tags the repository
   status after committing the release update with an annotated tag and
   the given annotation message. (defaults: ``False`` and
   ``"Version {{ new_version }}"``)
-  ``'tag'``: the name of the tag (default: the value of the
   ``new_version`` variable)

git-flow
''''''''

The ``git-flow`` VCS adapter follows the well-known git-flow workflow,
so the release is done starting from the ``develop`` branch, with a
dedicated release branch. There are currently no options for this
adapter.

Credits
-------

This package was created with Cookiecutter\_ and the
``audreyr/cookiecutter-pypackage``\ \_ project template.

-  Cookiecutter: https://github.com/audreyr/cookiecutter
-  ``audreyr/cookiecutter-pypackage``:
   https://github.com/audreyr/cookiecutter-pypackage

.. |Build Status| image:: https://travis-ci.org/lgiordani/punch.svg?branch=master
   :target: https://travis-ci.org/lgiordani/punch
.. |Version| image:: https://img.shields.io/pypi/v/punch.svg
   :target: https://github.com/lgiordani/punch
