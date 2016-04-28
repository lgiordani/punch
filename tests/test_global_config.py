import os
import mock
from punch import global_config as gc


def test_global_config_init_includes_env():
    with mock.patch.dict(os.environ, {"PUNCH_TEST_VAR": "Just a test variable"}):
        config = gc.GlobalConfig()
        assert config.format("---{$PUNCH_TEST_VAR}---") == "---Just a test variable---"


def test_global_config_can_add_a_variable():
    config = gc.GlobalConfig()
    config.add_variable("release_name", "Just a custom string")
    assert config.format("---{release_name}---") == "---Just a custom string---"


def test_global_config_can_add_a_dict():
    config = gc.GlobalConfig()
    config.add_dict({"release_name": "Just a custom string", "major": '5'})
    assert config.format("---{release_name}-{major}---") == "---Just a custom string-5---"
