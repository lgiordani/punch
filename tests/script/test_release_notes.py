import pytest

pytestmark = pytest.mark.slow

version_file_content = """
major = 1
minor = 0
patch = 0
"""

config_file_content_single_file = """
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

config_file_content_multiple_files = """
__config_version__ = 1

GLOBALS = {
    'serializer': {
        'semver': '{{major}}.{{minor}}.{{patch}}',
    }
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']

RELEASE_NOTES = [
    ('HISTORY.rst', r'^{{semver}} \\('),
    ('HISTORY.md', r'^## {{semver}} \\(')
]
"""

history_rst_file_wrong = """
=======
History
=======

1.0.0 (1980-01-01)
------------------

* Initial version
"""

history_md_file_wrong = """
# History

## 1.0.0 (1980-01-01)

* Initial version
"""

history_rst_file_correct = """
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

history_md_file_correct = """
# History

## 1.0.0 (1980-01-01)

* Initial version

## 2.0.0 (1980-01-01)

* Second version
"""


def test_release_notes_are_correct_single_file(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")
    test_environment.ensure_file_is_present(
        "HISTORY.rst", history_rst_file_correct)

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_single_file
    )

    out = test_environment.call([
        "punch",
        "--action", "punch:increase",
        "--action-options", "part=major"
    ])

    assert out.returncode == 0


def test_release_notes_are_correct_multiple_files(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")
    test_environment.ensure_file_is_present(
        "HISTORY.rst", history_rst_file_correct)
    test_environment.ensure_file_is_present(
        "HISTORY.md", history_md_file_correct)

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_multiple_files
    )

    out = test_environment.call([
        "punch",
        "--action", "punch:increase",
        "--action-options", "part=major"
    ])

    assert out.returncode == 0


def test_release_notes_are_wrong_single_file(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")
    test_environment.ensure_file_is_present(
        "HISTORY.rst", history_rst_file_wrong)

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_single_file
    )

    out = test_environment.call([
        "punch",
        "--action", "punch:increase",
        "--action-options", "part=major"
    ])

    assert out.returncode == 1
    assert "  * HISTORY.rst" in out.stdout


def test_release_notes_are_wrong_multiple_files(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")
    test_environment.ensure_file_is_present(
        "HISTORY.rst", history_rst_file_wrong)
    test_environment.ensure_file_is_present(
        "HISTORY.md", history_md_file_wrong)

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_multiple_files
    )

    out = test_environment.call([
        "punch",
        "--action", "punch:increase",
        "--action-options", "part=major"
    ])

    assert out.returncode == 1
    assert "  * HISTORY.rst" in out.stdout
    assert "  * HISTORY.md" in out.stdout
