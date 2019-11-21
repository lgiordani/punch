## Actions

Sometimes complex work flows are required, especially when `date` parts are involved. Those fields come from an external source (the system clock), and their updated status is thus unpredictable. You can obviously say at each execution if the field will be updated or not, but the link between the command line options and the updates performed by Punch is in general not evident.

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

This captures a situation where `build`, which is hierarchically lower than `year`, is reset when `year` changes. 

During the year the command issued by the user is `punch --part build`, which updates `build` and leaves `year` untouched, creating versions like `2019.0`, `2019.1`, and so on.

On the 1st of January of the new year, the command has to be `punch --part year`, otherwise the `year` part doesn't get modified, and `part` doesn't get reset. If we run this last command during the year, however, doesn't solve the issue, as `year` doesn't change, and `build` is not incremented. As mentioned before, this happens because date version parts are updated from an external source, which is unpredictable.

Punch allows to define actions, that is specific work flows that cannot be captured by the standard syntax. The only possible action type at the moment is `conditional_reset`.

Actions are defined by an `ACTIONS` dictionary in the configuration file, with the following syntax

``` python
ACTIONS = {
    'my_action_name': {
        'type': 'action_type',
        # ...
    }
}
```

where `my_action_name` is a free name that represents the action in your specific setup and `action_type` can only be `conditional_reset` at the moment. The dictionary can contain other keys required or supported by the specific action type.

### Conditional reset

``` python
GLOBALS = {
    'serializer': '{{year}}.{{month}}-{{build}}',
}

FILES = ["README.md"]

VERSION = [
    {
        'name': 'year',
        'type': 'date',
        'fmt': '%Y'
    },
    {
        'name': 'month',
        'type': 'date',
        'fmt': '%m'
    },
    'build'
]
ACTIONS = {
    'mbuild': {
        'type': 'conditional_reset',
        'field': 'build',
        'update_fields': ['year', 'month']
    }
}
```

The `conditional_reset` action work flow is the following

1. Update all the fields listed in `update_fields`.
2. If the full version changed, reset `field`. Otherwise just increment it.

So for the above configuration if the current version is `2017.01-4` on 31 January 2017 the command `punch --action mbuild` creates version `2017.01-5` (`year` and `month` do not change, so `build` is incremented), while on the 01 February 2017 it will create version `2017.02-0` (`month` changed and with it the full version, so `build` is reset).

## Release notes

Punch can check if your release notes are in sync with the version that will be created or not. If this option is enabled, Punch requires the release notes files to already contain the entry before the version is created. This was decided to avoid interrupting the flow, requiring a double execution of Punch, and generally making the work flow more complex (not to mention error management).

You can specify the `RELEASE_NOTES` **list** in the configuration file, each entry of which is a tuple with a file name and a regular expression. The regular expression can (and probably should) mention one of the serializers.

When Punch runs, it renders the regular expression string as a Jinja template, using the new version as rendered by the named serializer. Then it scans the associated file, looking for matches. If there are no matches, Punch exits with an error.

Example:

``` python
__config_version__ = 1

GLOBALS = {
    'serializer': {
        'semver': '{{major}}.{{minor}}.{{patch}}',
    }
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']

RELEASE_NOTES = [
    ('HISTORY.rst', r'^{{semver}} \\(')
]
```

In this example, if the new version returned by the `'semver'` serializer is `'2.0.0'`, Punch scans the `HISTORY.rst` file with the `r'^2.0.0 \\(` regular expression. If that file' content is something like

```
=======
History
=======

1.0.0 (1980-01-01)
------------------

* Initial version

2.0.0 (1980-01-01)
------------------

* Second version
```

Punch finds a match and continues, otherwise it interrupts the process before applying any change.

Another way to manage release notes is to replace a fixed string that you already have in the release notes file, as described by the example in the Complex serializers section below.

## Complex serializers

Punch assumes that each serializer represents both the search and the replacement patterns, filling the given template respectively with the old and the new version. Sometimes this is not true, so you can express more complex configurations with this syntax

``` python
GLOBALS = {
    'serializer': {
        'semver': {
            'search': 'Next Release',
            'replace': '{{major}}.{{minor}}.{{patch}}'
        }
    },
}
```

Where `search` is the pattern used to find the old version and `replace` is the pattern used to replace it. In this example the `search` pattern is a fixed string, but can use the usual Jinja2 syntax with the version fields. Complex serializers are supported in the configuration of single files as well

``` python
GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = [
    {
        'path': "CHANGELOG.rst",
        'serializer': {
            'semver': {
                'search': 'Next Release',
                'replace': '{{major}}.{{minor}}.{{patch}}'
            },
        }
    }
]
```
