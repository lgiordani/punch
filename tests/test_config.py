import os
import pytest

from punch import config as pc


@pytest.fixture
def config_file_content_without_globals_without_files():
    return """
__config_version__ = 1


VERSION = [
    {
        'name': 'major',
        'type': 'integer'
    },
    {
        'name': 'minor',
        'type': 'integer'
    },
    {
        'name': 'patch',
        'type': 'integer'
    }
]
"""


@pytest.fixture
def config_file_content_without_globals_without_version():
    return """
__config_version__ = 1


FILES = [
    'pkg/__init__.py',
    {
        'path': 'version.txt',
        'serializer': '{{major}}.{{minor}}'
    }
]
"""


@pytest.fixture
def config_file_content_without_globals():
    return """
__config_version__ = 1


FILES = [
    'pkg/__init__.py',
    {
        'path': 'version.txt',
        'serializer': '{{major}}.{{minor}}'
    }
]

VERSION = [
    {
        'name': 'major',
        'type': 'integer'
    },
    {
        'name': 'minor',
        'type': 'integer'
    },
    {
        'name': 'patch',
        'type': 'integer'
    }
]
"""


@pytest.fixture
def config_file_content(config_file_content_without_globals):
    return config_file_content_without_globals + """
# http://semver.org/
GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}'
}
"""


@pytest.fixture
def config_file_content_with_actions(config_file_content):
    return config_file_content + """

ACTIONS = {
    'mbuild': {
        'type': 'refresh',
        'refresh_fields': ['year', 'month'],
        'fallback_field': 'build'
    }
}
"""


@pytest.fixture
def config_file_content_with_vcs(config_file_content):
    return config_file_content + """

VCS = {
    'name': 'git',
    'commit_message': "Version updated to {{ new_version }}",
    'options': {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': '',
    }
}
"""


@pytest.fixture
def config_file_content_with_vcs_and_serializer(config_file_content):
    return config_file_content + """

VCS_SERIALIZER = 'main'

VCS = {
    'name': 'git',
    'commit_message': "Version updated to {{ new_version }}",
    'options': {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': '',
    }
}
"""


@pytest.fixture
def config_file_content_with_wrong_vcs(config_file_content):
    return config_file_content + """

VCS = {
    'commit_message': "Version updated to {{ new_version }}",
    'options': {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': '',
    }
}
"""


@pytest.fixture
def config_file_content_with_release_notes(config_file_content):
    return config_file_content + """

RELEASE_NOTES = [
    ('HISTORY.rst', '^{{version}} (')
]
"""


@pytest.fixture
def empty_file_content():
    return """
"""


@pytest.fixture
def version_file_content():
    return """
major = 1
minor = 5
patch = 0
"""


@pytest.fixture
def illegal_config_file_content():
    return """
__config_version__ = 2
"""


@pytest.fixture
def config_file_name():
    return 'punch_config.py'


@pytest.fixture
def version_file_name():
    return 'punch_version.py'


def clean_previous_imports():
    import sys

    for i in ['punch_config', 'punch_version']:
        if i in sys.modules:
            sys.modules.pop(i)


def write_file(dir, content, config_file_name):
    with open(os.path.join(dir, config_file_name), 'w') as f:
        f.write(content)


def test_read_empty_config_file(temp_empty_dir, empty_file_content,
                                config_file_name, version_file_content,
                                version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, empty_file_content, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    with pytest.raises(ValueError) as exc:
        pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert str(exc.value) == \
        "Given config file is invalid: missing '__config_version__' variable"


def test_read_illegal_config_file(temp_empty_dir, illegal_config_file_content,
                                  config_file_name, version_file_content,
                                  version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, illegal_config_file_content, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    with pytest.raises(pc.ConfigurationVersionError) as exc:
        pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert str(exc.value) == "Unsupported configuration file version 2"


def test_read_plain_variables(temp_empty_dir, config_file_content,
                              config_file_name, version_file_content,
                              version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert cf.__config_version__ == 1


def test_read_global_variables_without_globals(
        temp_empty_dir,
        config_file_content_without_globals,
        config_file_name, version_file_content,
        version_file_name):
    clean_previous_imports()

    write_file(
        temp_empty_dir,
        config_file_content_without_globals,
        config_file_name
    )
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert cf.globals == {}


def test_read_global_variables(temp_empty_dir, config_file_content,
                               config_file_name, version_file_content,
                               version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    expected_dict = {
        'serializer': '{{major}}.{{minor}}.{{patch}}'
    }

    assert cf.globals == expected_dict


def test_read_files_missing_files(
        temp_empty_dir, config_file_content_without_globals_without_files,
        config_file_name, version_file_content, version_file_name):
    clean_previous_imports()

    write_file(
        temp_empty_dir,
        config_file_content_without_globals_without_files,
        config_file_name
    )
    write_file(temp_empty_dir, version_file_content, version_file_name)

    with pytest.raises(ValueError):
        pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))


def test_read_files(temp_empty_dir, config_file_content, config_file_name,
                    version_file_content, version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert len(cf.files) == 2
    assert [fc.path for fc in cf.files] == ['pkg/__init__.py', 'version.txt']


def test_read_version_missing_version(
        temp_empty_dir, config_file_content_without_globals_without_version,
        config_file_name, version_file_content, version_file_name):
    clean_previous_imports()

    write_file(
        temp_empty_dir,
        config_file_content_without_globals_without_version,
        config_file_name
    )
    write_file(temp_empty_dir, version_file_content, version_file_name)

    with pytest.raises(ValueError):
        pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))


def test_read_version(temp_empty_dir, config_file_content, config_file_name,
                      version_file_content, version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    expected_value = [
        {
            'name': 'major',
            'type': 'integer'
        },
        {
            'name': 'minor',
            'type': 'integer'
        },
        {
            'name': 'patch',
            'type': 'integer'
        }
    ]

    assert cf.version == expected_value


def test_read_config_missing_vcs(temp_empty_dir, config_file_content,
                                 config_file_name, version_file_content,
                                 version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert cf.vcs is None


def test_read_vcs(temp_empty_dir, config_file_content_with_vcs,
                  config_file_name, version_file_content,
                  version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content_with_vcs, config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    expected_dict = {
        'name': 'git',
        'commit_message': "Version updated to {{ new_version }}",
        'options': {
            'make_release_branch': False,
            'annotate_tags': False,
            'annotation_message': '',
        }
    }

    assert cf.vcs == expected_dict
    assert cf.vcs_serializer == '0'


def test_read_vcs_with_serializer(
        temp_empty_dir, config_file_content_with_vcs_and_serializer,
        config_file_name, version_file_content,
        version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content_with_vcs_and_serializer,
               config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    expected_dict = {
        'name': 'git',
        'commit_message': "Version updated to {{ new_version }}",
        'options': {
            'make_release_branch': False,
            'annotate_tags': False,
            'annotation_message': '',
        }
    }

    assert cf.vcs == expected_dict
    assert cf.vcs_serializer == 'main'


def test_read_vcs_missing_name(temp_empty_dir,
                               config_file_content_with_wrong_vcs,
                               config_file_name, version_file_content,
                               version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content_with_wrong_vcs,
               config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    with pytest.raises(ValueError) as exc:
        pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert str(exc.value) == "Missing key 'name' in VCS configuration"


def test_read_empty_actions(temp_empty_dir, config_file_content,
                            config_file_name, version_file_content,
                            version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content,
               config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert 'punch:increase' in cf.actions
    assert 'punch:set' in cf.actions


def test_read_actions(temp_empty_dir, config_file_content_with_actions,
                      config_file_name, version_file_content,
                      version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content_with_actions,
               config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert 'punch:increase' in cf.actions
    assert 'punch:set' in cf.actions
    assert 'mbuild' in cf.actions


def test_read_release_notes(temp_empty_dir,
                            config_file_content_with_release_notes,
                            config_file_name, version_file_content,
                            version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content_with_release_notes,
               config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    expected = [
        ('HISTORY.rst', '^{{version}} (')
    ]

    assert cf.release_notes == expected


def test_read_release_notes_not_present(temp_empty_dir,
                                        config_file_content,
                                        config_file_name, version_file_content,
                                        version_file_name):
    clean_previous_imports()

    write_file(temp_empty_dir, config_file_content,
               config_file_name)
    write_file(temp_empty_dir, version_file_content, version_file_name)

    cf = pc.PunchConfig(os.path.join(temp_empty_dir, config_file_name))

    assert cf.release_notes == []
