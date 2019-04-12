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
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']
"""


def test_use_undefined_action(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    out = test_environment.call([
        "punch",
        "--action", "punch:foobar",
        "--action-options", "part=major"
    ])

    assert out.returncode == 1