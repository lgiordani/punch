import pytest
import mock
import io

from punch import replacer

file_content = """# Just a comment
__version__ = "1.0.0"
"""

updated_file_content = """# Just a comment
__version__ = "1.0.1"
"""


@pytest.fixture
def file_like():
    return io.StringIO(file_content)


def test_replace_content_without_config():
    with pytest.raises(TypeError):
        replacer.Replacer()


def test_replace_content_without_formatting(file_like):
    config = mock.Mock()
    config.GLOBALS = {}

    search_pattern = "__version__ = \"1.0.0\""
    replace_pattern = "__version__ = \"1.0.1\""
    old_file_content = file_like.read()
    rep = replacer.Replacer(config)

    new_file_content = rep.replace(old_file_content, search_pattern, replace_pattern)

    assert new_file_content == updated_file_content


def test_replace_content_with_formatting(file_like):
    config = mock.Mock()

    config.GLOBALS = {
        'current_version': "\"1.0.0\"",
        'new_version': "\"1.0.1\""
    }

    search_pattern = "__version__ = {current_version}"
    replace_pattern = "__version__ = {new_version}"
    old_file_content = file_like.read()
    rep = replacer.Replacer(config)

    new_file_content = rep.replace(old_file_content, search_pattern, replace_pattern)

    assert new_file_content == updated_file_content
