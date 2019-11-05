import subprocess
import pytest

pytestmark = pytest.mark.slow

test_name = "Test Name"

test_description = """
Bla bla bla
Multiple lines of bla bla
"""

system_year = subprocess.check_output(['date', '+%Y'])
system_year = system_year.decode('utf8').replace('\n', '')

system_month = subprocess.check_output(['date', '+%m'])
system_month = system_month.decode('utf8').replace('\n', '')

version_file_content = """
year = '{}'
month = '{}'
build = 0
""".format(system_year, system_month)

config_file_content = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{year}}.{{month}}.{{build}}',
}

FILES = ["README.md"]

ACTIONS = {
    'mbuild': {
        'type': 'conditional_reset',
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

test_files = {
    'README.md': {
        'original': "Version {}.{}.0.".format(system_year, system_month),
        'expected': "Version {}.{}.1.".format(system_year, system_month)
    }
}


@pytest.mark.parametrize("test_file", ["README.md"])
def test_action_refresh(script_runner, test_environment, test_file):
    test_environment.ensure_file_is_present(
        test_file,
        test_files[test_file]['original']
    )

    test_environment.ensure_file_is_present("punch_version.py",
                                            version_file_content)

    test_environment.ensure_file_is_present("punch_config.py",
                                            config_file_content)

    ret = test_environment.call(['punch', '--action', 'mbuild'])

    assert not ret.stderr
    assert test_environment.get_file_content(test_file) == \
        test_files[test_file]['expected']