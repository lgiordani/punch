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

illegal_config_file_content = """
__config_version__ = 2
"""

CONFIG_FILE_NAME = 'punch_config.py'


@pytest.fixture
def dir_with_config_file(temp_empty_uninitialized_dir):
    with open(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME), 'w') as f:
        f.write(config_file_content)

    return temp_empty_uninitialized_dir


@pytest.fixture
def dir_with_illegal_config_file(temp_empty_uninitialized_dir):
    with open(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME), 'w') as f:
        f.write(illegal_config_file_content)

    return temp_empty_uninitialized_dir


def test_read_illegal_config_file(dir_with_illegal_config_file):
    with pytest.raises(ValueError) as exc:
        cfr.ConfigFile(os.path.join(dir_with_illegal_config_file, CONFIG_FILE_NAME))

    assert str(exc.value) == "Unsupported configuration file version 2"


def test_read_plain_variables(dir_with_config_file):
    cf = cfr.ConfigFile(os.path.join(dir_with_config_file, CONFIG_FILE_NAME))

    assert cf.configuration.__config_version__ == 1


def test_read_complex_variables(dir_with_config_file):
    cf = cfr.ConfigFile(os.path.join(dir_with_config_file, CONFIG_FILE_NAME))

    expected_dict = {
        'parser': '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)',
        'current_version': "1.0.0"
    }

    assert cf.configuration.GLOBALS == expected_dict


