I think that your use case can be described by the following workflow: when updating `build` first check `month` and:

* if `month` changes, just carry on with that (changing `month` also resets `build` because of hierarchy)
* if `month` doesn't change, change `build`

So, with a version like `2017.05.6` a `--part build` issued in May will create version `2017.05.6`, while the same command in June will create version `2017.06.0`.

The two parts, `month` and `build`, are already linked in a hierarchical way, and this makes `build` reset when `month` changes.
What you need is the possibility to also link them in a reverse order, i.e. when `build` changes, refresh `month`.
I use "refresh" and not "change" as the two actions are different. This is something that only `date` version parts can do, as their value is given by an external condition.

I think the solution should address if possible all fields that depend on an external source, even if at the moment only `date` fields fall into this category. 

So one possible solution is: an `always-refresh` option on date parts which makes them refresh every time the version is bumped. We need however a mechanism to know if the version part containing a date has been changed, and act accordingly.

This is far from the current mechanism, so it would be useful to find something that works in a more seamless way with the current code. What I mean is that I am asking punch to update `build`, and I expect it to perform that and possibily other actions after it, but not to avoid it.

Another solution could be that of linking back from `build` to `month`, telling Punch to update month when I ask for `build`, which however breaks the usual behaviour of `--part`.

As in general we could have different fields that depend on external sources another solution could be to first update some or all of them, then to possibily carry on with the specific change asked with `--part`. The command line could be

`punch.py --part build --refresh month`

which however leads to another problem. If `month` gets refreshed (i.e. it changes because the external source gives us a different value) should we perform the `build` update? The two are hierarchically linked, so updating `month` makes `build` reset, and if I update it I end up with too many changes like

`2017.4.7 -- update month --> 2017.5.0 -- update build --> 2017.5.1`

This could be acceptable but it is far from being perfect, as the `build` part is configured to start with `0`.

I think it is possible to perform a double action:

* first refresh all the parts that are listed after `--refresh`, in order. If the version has changed stop here
* then carry on with the update expressed by `--part`

Another solution could be to allow the user to create an `action` that specifies a set of updates, but the problem is that the behaviour we want here is linked to external fields.

So:

* The behaviour is specific for some fields, just `date` at the moment.
* The mechanism shall work with the current hierarchical update
* It shall be explicit
* The command given by the user should be meaningful, i.e. it should perform what the user asks.

The best solution is to create a custom command in the config that lists the field(s) that shall be refreshed, and an alternative part to update like

``` python
ACTIONS = {
    'mbuild': {
        'type': 'refresh',
        'refresh_fields': ['year', 'month'],
        'fallback_field': 'build'
    }
}
```

This refreshes `year` and `month` and prepares the new version number. If this is different from the old one this is the new version, otherwise the process continues and issues a `--part build`.

If you try to list in `refresh_fields` a part that is not externally specified (like a date), Punch shall complain. 


-------------------------

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
}

FILES = [
    'version.txt',
    {
        'path': 'HISTORY.rst',
        'serializer': '{{ major }}.{{ minor }}'
    }
]
```

is equal to 

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
}

FILES = [
    'version.txt',
    {
        'path': 'HISTORY.rst',
        'strategy' : {
            'type': 'replace',
            'serializers' : ['{{ major }}.{{ minor }}']
        }
    }
]
```

Now we can introduce new strategies like

``` python
GLOBALS = {
    'serializer': '{{ major }}.{{ minor }}.{{ patch }}'
}

FILES = [
    'version.txt',
    {
        'path': 'HISTORY.rst',
        'strategy': {
            'type': 'insert_lines',
            'line': 5
            'content': [
                '{{ major }}.{{ minor }}',
                '-----------------------'
            ]
        }
    }
]
```


