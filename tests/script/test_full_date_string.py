import subprocess
import pytest

pytestmark = pytest.mark.slow

version_file_content = """
date = '20160415'
"""

config_file_content = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{date}}',
}

FILES = ["README.md"]

VERSION = [
    {
        'name': 'date',
        'type': 'date',
        'fmt': '%Y%m%d'
    }
]
"""


def test_update_date(test_environment, mocker):
    test_environment.ensure_file_is_present("README.md", "Version 20160415.")

    test_environment.ensure_file_is_present("punch_version.py",
                                            version_file_content)

    test_environment.ensure_file_is_present("punch_config.py",
                                            config_file_content)

    system_date = subprocess.check_output(['date', '+%Y%m%d'])

    system_date = system_date.decode('utf8').replace('\n', '')

    test_environment.call(["punch", "--part", "date"])

    assert test_environment.get_file_content("README.md") == \
        "Version {}.".format(system_date)
