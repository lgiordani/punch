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

VCS = {
    'name': 'git',
}
"""


def test_update_major(test_environment):
    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.output(["git", "init"])

    test_environment.output(["git", "add", "punch_config.py"])

    test_environment.output(["git", "commit", "-m", "some message"])

    test_environment.ensure_file_is_present("untracked_file")

    test_environment.call(["punch", "--part", "minor"])

    out = test_environment.output(
        ["git", "ls-tree", "-r", "master", "--name-only"]
    )

    assert "untracked_file" not in out
