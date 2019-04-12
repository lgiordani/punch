import subprocess
import pytest

pytestmark = pytest.mark.slow

version_file_content = """
year = '2016'
month = '04'
build = 1
"""

config_file_content = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{year}}.{{month}}.{{build}}',
}

FILES = ["README.md"]

ACTIONS = {
    'mbuild': {
        'field': 'build',
        'update_fields': ['year', 'month']
    }
}

VERSION = [
    {
        'name': 'year',
        'type': 'date',
        'fmt': '%Y'
    },
    {
        'name': 'month',
        'type': 'date',
        'fmt': '%m'
    },
    'build'
]
"""


def test_missing_action_type(script_runner, test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 2016.04.1.")

    test_environment.ensure_file_is_present("punch_version.py",
                                            version_file_content)

    test_environment.ensure_file_is_present("punch_config.py",
                                            config_file_content)

    system_year = subprocess.check_output(['date', '+%Y'])
    system_year = system_year.decode('utf8').replace('\n', '')

    system_month = subprocess.check_output(['date', '+%m'])
    system_month = system_month.decode('utf8').replace('\n', '')

    out = test_environment.call(['punch', '--action', 'mbuild'])

    assert out.returncode == 1
