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

