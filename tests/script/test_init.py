import pytest

pytestmark = pytest.mark.slow

version_file_content = """major = 0
minor = 1
patch = 0
"""

config_file_content = """__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = []

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git',
    'commit_message': (
        "Version updated from {{ current_version }}"
        " to {{ new_version }}")
}
"""


def test_init(test_environment):
    test_environment.call(["punch", "--init"])

    assert test_environment.get_file_content("punch_version.py") == \
        version_file_content

    assert test_environment.get_file_content("punch_config.py") == \
        config_file_content
