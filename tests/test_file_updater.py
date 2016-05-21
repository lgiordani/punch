import os
import six
import pytest

from punch import file_configuration as fc
from punch import file_updater as fu


@pytest.fixture
def temp_dir_with_version_file(temp_empty_dir):
    with open(os.path.join(temp_empty_dir, "__init__.py"), 'w') as f:
        f.write("__version__ = \"1.2.3\"")

    return temp_empty_dir


@pytest.fixture
def temp_dir_with_version_file_partial(temp_empty_dir):
    with open(os.path.join(temp_empty_dir, "__init__.py"), 'w') as f:
        f.write("__version__ = \"1.2\"")

    return temp_empty_dir


def test_file_updater(temp_dir_with_version_file):
    filepath = os.path.join(temp_dir_with_version_file, "__init__.py")

    current_version = {
        'major': 1,
        'minor': 2,
        'patch': 3
    }
    new_version = {
        'major': 1,
        'minor': 2,
        'patch': 4
    }

    local_variables = {
        'serializer': "__version__ = \"{{major}}.{{minor}}.{{patch}}\""
    }

    file_config = fc.FileConfiguration(filepath, local_variables)

    updater = fu.FileUpdater(file_config)
    updater.update(current_version, new_version)

    with open(filepath, 'r') as f:
        new_file_content = f.read()

    assert new_file_content == "__version__ = \"1.2.4\""


def test_file_updater_with_partial_serializer(temp_dir_with_version_file_partial):
    filepath = os.path.join(temp_dir_with_version_file_partial, "__init__.py")

    current_version = {
        'major': 1,
        'minor': 2,
        'patch': 3
    }
    new_version = {
        'major': 1,
        'minor': 3,
        'patch': 0
    }

    local_variables = {
        'serializer': "__version__ = \"{{major}}.{{minor}}\""
    }

    file_config = fc.FileConfiguration(filepath, local_variables)

    updater = fu.FileUpdater(file_config)
    updater.update(current_version, new_version)

    with open(filepath, 'r') as f:
        new_file_content = f.read()

    assert new_file_content == "__version__ = \"1.3\""


def test_file_updater_with_nonexisting_file(temp_empty_dir):
    filepath = os.path.join(temp_empty_dir, "__init__.py")
    local_variables = {
        'serializer': "__version__ = \"{{major}}.{{minor}}\""
    }

    file_config = fc.FileConfiguration(filepath, local_variables)

    current_version = {
        'major': 1,
        'minor': 2,
        'patch': 3
    }
    new_version = {
        'major': 1,
        'minor': 3,
        'patch': 0
    }

    if six.PY2:
        expected_exception = IOError
    else:
        expected_exception = FileNotFoundError

    with pytest.raises(expected_exception) as exc:
        updater = fu.FileUpdater(file_config)
        updater.update(current_version, new_version)

    assert str(exc.value) == "The file {} does not exist".format(file_config.path)


def test_file_updater_preview(temp_empty_dir):
    filepath = os.path.join(temp_empty_dir, "__init__.py")
    local_variables = {
        'serializer': "__version__ = \"{{major}}.{{minor}}\""
    }

    file_config = fc.FileConfiguration(filepath, local_variables)

    current_version = {
        'major': 1,
        'minor': 2,
        'patch': 3
    }
    new_version = {
        'major': 1,
        'minor': 3,
        'patch': 0
    }

    updater = fu.FileUpdater(file_config)
    summary = updater.get_summary(current_version, new_version)

    assert summary == [("__version__ = \"1.2\"", "__version__ = \"1.3\"")]
