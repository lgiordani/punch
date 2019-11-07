
## Examples from the tests

The following examples are automatically extracted from the test suite.


### Conditional Reset Action - Increment

This configuraton implements a version number that includes the current date
(`{{year}}.{{month}}`) and a `build`. The build gets reset every beginning
of the month.

The `conditional_reset` action can reset a field depending on what happens
to other fields. In this case the `build` field depends on `year` and `month`,
and since these are not updated, the former is incremented.

#### Version file
```
year = '2019'
month = '11'
build = 0
```

#### Configuration file
```
__config_version__ = 1

GLOBALS = {
    'serializer': '{{year}}.{{month}}.{{build}}',
}

FILES = ["README.md"]

ACTIONS = {
    'mbuild': {
        'type': 'conditional_reset',
        'field': 'build',
        'update_fields': ['year', 'month']
    }
}

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
```

#### Effects

Original `README.md`
```
Version 2019.11.0.
```
Final `README.md`
```
Version 2019.11.1.
```

### Conditional Reset Action - Reset

This configuraton implements a version number that includes the current date
(`{{year}}.{{month}}`) and a `build`. The build gets reset every beginning
of the month.

The `conditional_reset` action can reset a field depending on what happens
to other fields. In this case the `build` field depends on `year` and `month`,
and since these get updated the former is reset to 0.

#### Version file
```
year = '2018'
month = '11'
build = 0
```

#### Configuration file
```
__config_version__ = 1

GLOBALS = {
    'serializer': '{{year}}.{{month}}.{{build}}',
}

FILES = ["README.md"]

ACTIONS = {
    'mbuild': {
        'type': 'conditional_reset',
        'field': 'build',
        'update_fields': ['year', 'month']
    }
}

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
```

#### Effects

Original `README.md`
```
Version 2018.11.0.
```
Final `README.md`
```
Version 2019.11.0.
```
