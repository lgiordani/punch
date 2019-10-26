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
        'semver': '{{major}}.{{minor}}.{{patch}}',
    }
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']

RELEASE_NOTES = [
    ('HISTORY.rst', r'^{{semver}} \\(')
]
"""

history_file_wrong = """
=======
History
=======

1.0.0 (1980-01-01)
------------------

* Initial version
"""

history_file_correct = """
=======
History
=======

1.0.0 (1980-01-01)
------------------

* Initial version

2.0.0 (1980-01-01)
------------------

* Second version
"""


def test_missing_release_notes(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")
    test_environment.ensure_file_is_present("HISTORY.rst", history_file_wrong)

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
        "--action", "punch:increase",
        "--action-options", "part=major"
    ])

    assert out.returncode == 1


def test_release_notes_are_correct(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")
    test_environment.ensure_file_is_present(
        "HISTORY.rst", history_file_correct)

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
        "--action", "punch:increase",
        "--action-options", "part=major"
    ])

    assert out.returncode == 0
