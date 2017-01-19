import subprocess
import six
import pytest

if six.PY2:
    import mock
else:
    from unittest import mock

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


def test_update_major(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 2016.4.")

    test_environment.ensure_file_is_present("punch_version.py", version_file_content)

    test_environment.ensure_file_is_present("punch_config.py", config_file_content)

    system_year = subprocess.check_output(['date', '+%Y'])
    system_year = system_year.decode('utf8').replace('\n', '')

    system_month = subprocess.check_output(['date', '+%m'])
    system_month = system_month.decode('utf8').replace('\n', '').replace('0', '')

    test_environment.call(["punch", "--part", "major"])

    assert test_environment.get_file_content("README.md") == \
        "Version {}.{}.".format(system_year, system_month)


def test_update_minor(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 2016.4.")

    test_environment.ensure_file_is_present("punch_version.py", version_file_content)

    test_environment.ensure_file_is_present("punch_config.py", config_file_content)

    system_month = subprocess.check_output(['date', '+%m'])
    system_month = system_month.decode('utf8').replace('\n', '').replace('0', '')

    test_environment.call(["punch", "--part", "minor"])

    assert test_environment.get_file_content("README.md") == \
        "Version 2016.{}.".format(system_month)
