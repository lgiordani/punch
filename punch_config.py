__config_version__ = 1

# http://semver.org/
GLOBALS = {
    #    'serializer': '{{major}}.{{minor}}.{{patch}}',
    'serializer': "{{major}}.{{minor}}.{{patch}}{{ '+%s' % build if build}}"
}

FILES = [
    'version.txt',
    # {
    #     'path': 'version.txt',
    #     'serializer': '{{major}}.{{minor}}'
    # },
    # {
    #     'path': 'version.txt',
    #     'serializer': '__version__ = {{ GLOBALS.serializer}}'
    # },
    # {
    #     'path': 'version.txt',
    #     'serializer': [
    #         'Full version: {{major}}.{{minor}}.{{patch}}',
    #         'Short version: {{major}}.{{minor}}'
    #     ]
    # }
]

VERSION = ['major', 'minor', 'patch',
           # {
           #     'name': 'build',
           #     'start_value': 1
           # }
           ]
