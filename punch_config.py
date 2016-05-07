__config_version__ = 1

# http://semver.org/
GLOBALS = {
#    'serializer': '{{major}}.{{minor}}.{{patch}}',
    'serializer': "{{major}}.{{minor}}.{{patch}}{{ '+%s' % build if build}}"
}

FILES = ['version.txt'
    # {
    #     'path': 'version.txt',
    #     'serializer': '{{major}}.{{minor}}'
    # }
]

#VERSION = ['major', 'minor', 'patch']
VERSION = ['major', 'minor', 'patch',
           {
               'name': 'build',
               'start_value': 1
           }]