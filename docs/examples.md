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
