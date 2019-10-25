import pytest

pytestmark = pytest.mark.slow

version_file_content = """
major = 1
minor = 0
patch = 0
"""

config_file_content_unnamed_serializer = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}'
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']
"""


config_file_content_named_serializer_with_main = """
__config_version__ = 1

GLOBALS = {
    'serializer': {
        'semver': '{{major}}.{{minor}}.{{patch}}',
    },
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']
"""


def test_unnamed_serializer(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_named_serializer_with_main
    )

    out = test_environment.call(["punch", "--part", "major"])

    assert out.returncode == 0


def test_named_serializer_with_main_serializers(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_named_serializer_with_main
    )

    out = test_environment.call(["punch", "--part", "major"])

    assert out.returncode == 0
