import subprocess
import six
import pytest

if six.PY2:
    import mock
else:
    from unittest import mock

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


def test_update_date(test_environment):
    # mock_strftime.side_effect = lambda x: {'%Y%m%d': '20170102'}.get(x)

    test_environment.ensure_file_is_present("README.md", "Version 20160415.")

    test_environment.ensure_file_is_present("punch_version.py",
                                            version_file_content)

    test_environment.ensure_file_is_present("punch_config.py",
                                            config_file_content)

    system_date = subprocess.check_output(['date', '+%Y%m%d'])

    system_date = system_date.decode('utf8').replace('\n', '')

    with mock.patch('punch.version_part.strftime') as mock_strftime:
        mock_strftime.side_effect = ValueError
        test_environment.call(["punch", "--part", "date"])

    assert test_environment.get_file_content("README.md") == \
        "Version {}.".format(system_date)
