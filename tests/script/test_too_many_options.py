import subprocess

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


def test_specify_part_and_action(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    with pytest.raises(subprocess.CalledProcessError):
        test_environment.output([
            "punch",
            "--part", "major",
            "--action", "punch:increase",
            "--action-options", "part=major"
        ])


def test_specify_part_and_set_part(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    with pytest.raises(subprocess.CalledProcessError):
        test_environment.output([
            "punch",
            "--part", "major",
            "--set-part", "major=4",
        ])


def test_specify_set_part_and_action(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    with pytest.raises(subprocess.CalledProcessError):
        test_environment.output([
            "punch",
            "--set-part", "major=5",
            "--action", "punch:increase",
            "--action-options", "part=major"
        ])
