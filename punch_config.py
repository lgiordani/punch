__config_version__ = 1

# http://semver.org/
GLOBALS = {
    'serializer': '{major}.{minor}.{patch}'
}

FILES = [
    'pkg/__init__.py',
    {
        'path': 'version.txt',
        'serializer': '{major}.{minor}'
    }
]

VERSION = [
    {
        'name': 'major',
        'type': 'integer'
    },
    {
        'name': 'minor',
        'type': 'integer'
    },
    {
        'name': 'patch',
        'type': 'integer'
    }
]