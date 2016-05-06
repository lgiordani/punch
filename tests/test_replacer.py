import six

import pytest
import io

from punch import replacer


def file_like(file_content):
    if six.PY2:
        return io.StringIO(unicode(file_content))
    else:
        return io.StringIO(file_content)


def test_replace_content_without_config():
    with pytest.raises(TypeError):
        replacer.Replacer()


def test_replace_content():
    current_version = {
        'major': 1,
        'minor': 0,
        'patch': 0
    }
    new_version = {
        'major': 1,
        'minor': 0,
        'patch': 1
    }

    file_content = """# Just a comment
    __version__ = "1.0.0"
    """

    updated_file_content = """# Just a comment
    __version__ = "1.0.1"
    """

    serializer = "__version__ = \"{{major}}.{{minor}}.{{patch}}\""
    old_file_content = file_like(file_content).read()
    rep = replacer.Replacer(serializer)

    new_file_content = rep.replace(old_file_content, current_version, new_version)

    assert new_file_content == updated_file_content


def test_replace_content_without_using_all_parts():
    current_version = {
        'major': 1,
        'minor': 0,
        'patch': 0
    }
    new_version = {
        'major': 1,
        'minor': 1,
        'patch': 0
    }

    file_content = """# Just a comment
    __version__ = "1.0"
    """

    updated_file_content = """# Just a comment
    __version__ = "1.1"
    """

    serializer = "__version__ = \"{{major}}.{{minor}}\""
    old_file_content = file_like(file_content).read()
    rep = replacer.Replacer(serializer)

    new_file_content = rep.replace(old_file_content, current_version, new_version)

    assert new_file_content == updated_file_content
