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


def test_get_versions():
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

    serializer = "__version__ = \"{{major}}.{{minor}}.{{patch}}\""
    rep = replacer.Replacer(serializer)

    list_of_versions = rep.run_all_serializers(current_version, new_version)

    assert list_of_versions == [("__version__ = \"1.0.0\"", "__version__ = \"1.0.1\"")]


def test_get_versions_with_multiple_serializers():
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

    serializers = [
        "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        "__api_abi__ = \"{{major}}.{{minor}}\""
    ]
    rep = replacer.Replacer(serializers)

    list_of_versions = rep.run_all_serializers(current_version, new_version)

    assert list_of_versions == [
        ("__version__ = \"1.0.0\"", "__version__ = \"1.0.1\""),
        ("__api_abi__ = \"1.0\"", "__api_abi__ = \"1.0\"")
    ]


def test_get_main_version_change_with_multiple_serializers():
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

    serializers = [
        "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        "__api_abi__ = \"{{major}}.{{minor}}\""
    ]
    rep = replacer.Replacer(serializers)

    current, new = rep.run_main_serializer(current_version, new_version)

    assert current, new == ("__version__ = \"1.0.0\"", "__version__ = \"1.0.1\"")


def test_replace_content_with_multiple_serializers():
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
    __api_abi__ = "1.0"
    """

    updated_file_content = """# Just a comment
    __version__ = "1.0.1"
    __api_abi__ = "1.0"
    """

    serializers = [
        "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        "__api_abi__ = \"{{major}}.{{minor}}\""
    ]

    old_file_content = file_like(file_content).read()
    rep = replacer.Replacer(serializers)

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
