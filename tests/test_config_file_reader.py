import os
import pytest

from punch import config_file_reader as cfr


@pytest.fixture
def semver_config_file_content():
    return """
__config_version__ = 1

# http://semver.org/
GLOBALS = {
    'serializer': '{major}.{minor}.{patch}'
}

FILES = [
    'pkg/__init__.py',
    {
        'path': 'version.txt',
        'serializer': '{major}.{minor}'
    }
]

VERSION = [
    {
        'name': 'major',
        'value': 1,
        'type': 'integer'
    },
    {
        'name': 'minor',
        'value': 5,
        'type': 'integer'
    },
    {
        'name': 'patch',
        'value': 0,
        'type': 'integer'
    }
]
"""


@pytest.fixture
def empty_config_file_content():
    return """
"""


@pytest.fixture
def illegal_config_file_content():
    return """
__config_version__ = 2
"""


CONFIG_FILE_NAME = 'punch_config.py'


def write_config_file(dir, content):
    with open(os.path.join(dir, CONFIG_FILE_NAME), 'w') as f:
        f.write(content)


def test_read_empty_config_file(temp_empty_uninitialized_dir, empty_config_file_content):
    write_config_file(temp_empty_uninitialized_dir, empty_config_file_content)

    with pytest.raises(ValueError) as exc:
        cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME))

    assert str(exc.value) == "Given config file is invalid: missing '__config_version__' attribute"


def test_read_illegal_config_file(temp_empty_uninitialized_dir, illegal_config_file_content):
    write_config_file(temp_empty_uninitialized_dir, illegal_config_file_content)

    with pytest.raises(ValueError) as exc:
        cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME))

    assert str(exc.value) == "Unsupported configuration file version 2"


def test_read_plain_variables(temp_empty_uninitialized_dir, semver_config_file_content):
    write_config_file(temp_empty_uninitialized_dir, semver_config_file_content)

    cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME))

    assert cf.__config_version__ == 1


def test_read_global_variables(temp_empty_uninitialized_dir, semver_config_file_content):
    write_config_file(temp_empty_uninitialized_dir, semver_config_file_content)

    cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME))

    expected_dict = {
        'serializer': '{major}.{minor}.{patch}'
    }

    assert cf.globals == expected_dict


def test_read_version(temp_empty_uninitialized_dir, semver_config_file_content):
    write_config_file(temp_empty_uninitialized_dir, semver_config_file_content)

    cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME))

    assert len(cf.version.parts) == 3


# def test_read_files(temp_empty_uninitialized_dir, semver_config_file_content):
#     write_config_file(temp_empty_uninitialized_dir, semver_config_file_content)
#
#     cf = cfr.ConfigFile(os.path.join(temp_empty_uninitialized_dir, CONFIG_FILE_NAME))
#
#     assert len(cf.files) == 2
