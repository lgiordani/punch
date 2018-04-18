import os
import subprocess

import pytest

import punch.version as ver
import punch.version_part as vpart

pytestmark = pytest.mark.slow

version_file_content = """
major = '2016'
minor = '4'
"""

config_file_content = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}',
}

FILES = ["README.md"]

VERSION = [
    {
        'name': 'major',
        'type': 'date',
        'fmt': 'YYYY'
    },
    {
        'name': 'minor',
        'type': 'date',
        'fmt': 'MM'
    }
]
"""


@pytest.fixture
def version_mm():
    v = ver.Version()
    v.create_part('major', '2018', vpart.DateVersionPart, '%Y')
    v.create_part('minor', '04', vpart.DateVersionPart, '%m')
    return v


def clean_previous_imports():
    import sys

    for i in ['punch_config', 'punch_version']:
        if i in sys.modules:
            sys.modules.pop(i)


def test_update_major(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 2016.4.")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    system_year = subprocess.check_output(['date', '+%Y'])
    system_year = system_year.decode('utf8').replace('\n', '')

    system_month = subprocess.check_output(['date', '+%m'])
    system_month = system_month.decode('utf8').\
        replace('\n', '').lstrip('0')

    test_environment.call(["punch", "--part", "major"])

    assert test_environment.get_file_content("README.md") == \
        "Version {}.{}.".format(system_year, system_month)


def test_update_minor(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 2016.4.")

    test_environment.ensure_file_is_present(
        "punch_version.py", version_file_content)

    test_environment.ensure_file_is_present(
        "punch_config.py", config_file_content)

    system_month = subprocess.check_output(['date', '+%m'])
    system_month = system_month.decode(
        'utf8').replace('\n', '').lstrip('0')

    test_environment.call(["punch", "--part", "minor"])

    assert test_environment.get_file_content("README.md") == \
        "Version 2016.{}.".format(system_month)


def test_write_version_file(temp_empty_dir, version_mm):
    clean_previous_imports()

    version_filepath = os.path.join(temp_empty_dir, 'punch_version.py')

    version_mm.to_file(version_filepath)

    with open(version_filepath, 'r') as f:
        content = sorted(f.readlines())

    # Uncomment to get more insight into test failures.
    # print(content)

    expected_content = [
        "major = '2018'\n",
        "minor = '04'\n",
    ]

    assert content == expected_content
