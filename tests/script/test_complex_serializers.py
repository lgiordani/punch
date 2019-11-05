import pytest

pytestmark = pytest.mark.slow

version_file_content = """
major = 1
minor = 0
patch = 0
"""

config_file_content = """
__config_version__ = 1

GLOBALS = {
    'serializer': {
        'semver': {
            'search': 'Next Release',
            'replace': '{{major}}.{{minor}}.{{patch}}'
        }
    },
}

FILES = ["CHANGELOG.rst"]

VERSION = ['major', 'minor', 'patch']
"""

config_file_content_dedicated_serializer = """
__config_version__ = 1

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

VERSION = ['major', 'minor', 'patch']
"""

changelog = """
Changelog
=========

Next Release
------------
**Added**

* Added some new feature
"""

expected_changelog = """
Changelog
=========

2.0.0
------------
**Added**

* Added some new feature
"""


def test_complex_serializer(test_environment):
    test_environment.ensure_file_is_present("CHANGELOG.rst", changelog)

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.call(["punch", "--part", "major"])

    assert test_environment.get_file_content("CHANGELOG.rst") == \
        expected_changelog


def test_complex_serializer_dedicated_serializers(test_environment):
    test_environment.ensure_file_is_present("CHANGELOG.rst", changelog)

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_dedicated_serializer
    )

    test_environment.call(["punch", "--part", "major"])

    assert test_environment.get_file_content("CHANGELOG.rst") == \
        expected_changelog
