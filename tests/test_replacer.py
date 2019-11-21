import six

import pytest
import io

from punch import replacer


def file_like(file_content):
    if six.PY2:
        return io.StringIO(unicode(file_content))  # NOQA
    else:
        return io.StringIO(file_content)


def test_replace_content_without_config():
    with pytest.raises(TypeError):
        replacer.Replacer()


def test_process_single_serializer_string():
    serializer = "__version__ = \"{{major}}.{{minor}}.{{patch}}\""

    rep = replacer.Replacer(serializer)

    assert rep.serializers == {
        '0': "__version__ = \"{{major}}.{{minor}}.{{patch}}\""
    }


def test_update_single_serializer_string():
    serializer = "__version__ = \"{{major}}.{{minor}}.{{patch}}\""

    rep = replacer.Replacer(serializer)

    rep.update("__version__ = \"{{major}}.{{minor}}\"")

    assert rep.serializers == {
        '0': "__version__ = \"{{major}}.{{minor}}\""
    }


def test_process_multiple_serializers_list():
    serializer = [
        "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        "__api_abi__ = \"{{major}}.{{minor}}\""
    ]

    rep = replacer.Replacer(serializer)

    assert rep.serializers == {
        '0': "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        '1': "__api_abi__ = \"{{major}}.{{minor}}\""
    }


def test_update_multiple_serializers_list():
    serializer = [
        "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        "__api_abi__ = \"{{major}}.{{minor}}\""
    ]

    rep = replacer.Replacer(serializer)

    rep.update([
        "__version__ = \"{{major}}.{{minor}}\"",
        "__major__ = \"{{major}}\""
    ])

    assert rep.serializers == {
        '0': "__version__ = \"{{major}}.{{minor}}\"",
        '1': "__major__ = \"{{major}}\""
    }


def test_process_multiple_serializers_dict():
    serializer = {
        'main': "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        'apiabi': "__api_abi__ = \"{{major}}.{{minor}}\""
    }

    rep = replacer.Replacer(serializer, 'main')

    assert rep.serializers == {
        'main': "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        'apiabi': "__api_abi__ = \"{{major}}.{{minor}}\""
    }


def test_update_multiple_serializers_dict():
    serializer = {
        'main': "__version__ = \"{{major}}.{{minor}}.{{patch}}\"",
        'apiabi': "__api_abi__ = \"{{major}}.{{minor}}\""
    }

    rep = replacer.Replacer(serializer, 'main')

    rep.update({
        'main': "__version__ = \"{{major}}.{{minor}}\"",
        'major': "__major__ = \"{{major}}\""
    })

    assert rep.serializers == {
        'main': "__version__ = \"{{major}}.{{minor}}\"",
        'apiabi': "__api_abi__ = \"{{major}}.{{minor}}\"",
        'major': "__major__ = \"{{major}}\""
    }


def test_process_serializers_wrong_type():
    serializer = 5

    with pytest.raises(TypeError):
        replacer.Replacer(serializer)


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
    rep = replacer.Replacer(serializer)

    new_file_content = rep.replace(file_content, current_version, new_version)

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

    changes = rep.run_all_serializers(current_version, new_version)

    assert changes == {
        '0': ("__version__ = \"1.0.0\"", "__version__ = \"1.0.1\"")
    }


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

    changes = rep.run_all_serializers(current_version, new_version)

    assert changes == {
        '0': ("__version__ = \"1.0.0\"", "__version__ = \"1.0.1\""),
        '1': ("__api_abi__ = \"1.0\"", "__api_abi__ = \"1.0\"")
    }


def test_get_specific_version_change_with_multiple_serializers():
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

    current, new = rep.run_serializer('0', current_version, new_version)

    assert current, new == (
        "__version__ = \"1.0.0\"", "__version__ = \"1.0.1\""
    )


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

    rep = replacer.Replacer(serializers)

    new_file_content = rep.replace(file_content, current_version, new_version)

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
    rep = replacer.Replacer(serializer)

    new_file_content = rep.replace(file_content, current_version, new_version)

    assert new_file_content == updated_file_content
