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


def test_set_part(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.call([
        "punch",
        "--action", "punch:set",
        "--action-options", "major=3"
    ])

    assert test_environment.get_file_content("README.md") == "Version 3.0.0"


# def test_set_part_reset_on_set(test_environment):
#     test_environment.ensure_file_is_present("README.md", "Version 1.2.3")

#     test_environment.ensure_file_is_present(
#         "punch_version.py",
#         version_file_content
#     )

#     test_environment.ensure_file_is_present(
#         "punch_config.py",
#         config_file_content
#     )

#     test_environment.call([
#         "punch",
#         "--action", "punch:set",
#         "--action-options", "major=9",
#         "--action-flags", "reset-on-set=true"
#     ])

#     assert test_environment.get_file_content("README.md") == "Version 9.0.0"


def test_punch_set_multiple_version_parts(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        "major = 1\nminor = 0\npatch = 0\n"
    )

    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["README.md"]

    VERSION = ['major', 'minor', 'patch']
    """

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.call([
        "punch",
        "--action", "punch:set",
        "--action-options", "minor=4,patch=23"
    ])

    assert test_environment.get_file_content("README.md") == "Version 1.4.23"


# def test_punch_set_and_reset_multiple_parts_fails(test_environment):
#     test_environment.ensure_file_is_present("README.md", "Version 1.2.3")

#     test_environment.ensure_file_is_present(
#         "punch_version.py",
#         "major = 1\nminor = 2\npatch = 3\n"
#     )

#     config_file_content = """
#     __config_version__ = 1

#     GLOBALS = {
#         'serializer': '{{major}}.{{minor}}.{{patch}}',
#     }

#     FILES = ["README.md"]

#     VERSION = ['major', 'minor', 'patch']
#     """

#     test_environment.ensure_file_is_present(
#         "punch_config.py",
#         config_file_content
#     )

#     with pytest.raises(subprocess.CalledProcessError):
#         test_environment.output(
#             ["punch", "--set-part", "major=9,minor=8", "--reset-on-set"])
