import pytest

from punch import file_configuration as fc

@pytest.fixture
def global_variables():
    return {
        'serializer': '{major}.{minor}.{patch}'
    }


def test_file_configuration_from_string(global_variables):
    fconf = fc.FileConfiguration('pkg/__init__.py')

    assert fconf.path == 'pkg/__init__.py'