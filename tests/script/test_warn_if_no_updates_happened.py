import pytest

pytestmark = pytest.mark.slow

version_file_content = """
major = 0
minor = 2
patch = 0
"""

config_file_content = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["VERSION"]

VERSION = ['major', 'minor', 'patch']
"""


def test_update_major(test_environment):
    # This is not matching the version_file_content on purpose
    test_environment.ensure_file_is_present("VERSION", "0.1.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    out = test_environment.output(["punch", "--part", "minor"])

    assert test_environment.get_file_content("VERSION") == "0.1.0"
    assert "Warning" in out
    assert "VERSION" in out
