import os
import pytest

from punch import config_file_reader as cfr

config_file_content = """
__config_version__ = 1

# http://semver.org/
GLOBALS = {
    'parser': '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
    'current_version': "1.0.0"
}

FILES = [
]
"""

CONFIG_FILE_NAME = 'punch_config.py'


@pytest.fixture
def dir_with_config_file(temp_empty_uninitialized_dir):
    with open(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME), 'w') as f:
        f.write(config_file_content)

    return temp_empty_uninitialized_dir


def test_read_config(dir_with_config_file):
    cf = cfr.ConfigFile(os.path.join(dir_with_config_file, CONFIG_FILE_NAME))

    assert cf.configuration.__config_version__ == 1
