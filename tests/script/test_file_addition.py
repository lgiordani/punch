import pytest

pytestmark = pytest.mark.slow

version_file_content = """
major = 0
minor = 2
patch = 0
"""


def test_check_no_silent_addition_happens(test_environment):
    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["VERSION"]

    VERSION = ['major', 'minor', 'patch']

    VCS = {
        'name': 'git',
    }
    """

    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.output(["git", "init"])

    test_environment.output(["git", "add", "punch_config.py"])

    test_environment.output(["git", "commit", "-m", "some message"])

    test_environment.ensure_file_is_present("untracked_file")

    test_environment.call(["punch", "--part", "minor"])

    out = test_environment.output(
        ["git", "ls-tree", "-r", "master", "--name-only"]
    )

    assert "untracked_file" not in out


def test_check_punch_git_relevant_files_are_always_added(test_environment):
    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["VERSION"]

    VERSION = ['major', 'minor', 'patch']

    VCS = {
        'name': 'git',
    }
    """

    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.call(["git", "init"])

    test_environment.call(["git", "add", "punch_config.py"])
    test_environment.call(["git", "add", "punch_version.py"])
    test_environment.call(["git", "add", "VERSION"])

    test_environment.call(["git", "commit", "-m", "Initial version"])

    ret = test_environment.call(["punch", "--part", "minor"])

    assert ret.success


def test_check_punch_git_flow_relevant_files_are_always_added(
        test_environment):
    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["VERSION"]

    VERSION = ['major', 'minor', 'patch']

    VCS = {
        'name': 'git-flow',
    }
    """

    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.call(["git", "init"])
    test_environment.call(["git", "flow", "init", "-d"])

    test_environment.call(["git", "add", "punch_config.py"])
    test_environment.call(["git", "add", "punch_version.py"])
    test_environment.call(["git", "add", "VERSION"])

    test_environment.call(["git", "commit", "-m", "Initial version"])

    ret = test_environment.call(["punch", "--part", "minor"])

    assert ret.success


def test_git_add_specific_file_to_commit(test_environment):
    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["VERSION"]

    VERSION = ['major', 'minor', 'patch']

    VCS = {
        'name': 'git',
        'include_files': ['HISTORY.rst']
    }
    """

    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.ensure_file_is_present("HISTORY.rst")

    test_environment.call(["git", "init"])

    test_environment.call(["git", "add", "punch_config.py"])
    test_environment.call(["git", "add", "punch_version.py"])
    test_environment.call(["git", "add", "VERSION"])

    test_environment.call(["git", "commit", "-m", "Initial version"])

    test_environment.call(["punch", "--part", "minor"])

    out = test_environment.output(
        ["git", "ls-tree", "-r", "master", "--name-only"]
    )

    assert "HISTORY.rst" in out


def test_git_add_all_files_to_commit(test_environment):
    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["VERSION"]

    VERSION = ['major', 'minor', 'patch']

    VCS = {
        'name': 'git',
        'include_all_files': True
    }
    """

    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.ensure_file_is_present("HISTORY.rst")

    test_environment.call(["git", "init"])

    test_environment.call(["git", "add", "punch_config.py"])
    test_environment.call(["git", "add", "punch_version.py"])
    test_environment.call(["git", "add", "VERSION"])

    test_environment.call(["git", "commit", "-m", "Initial version"])

    test_environment.call(["punch", "--part", "minor"])

    out = test_environment.output(
        ["git", "ls-tree", "-r", "master", "--name-only"]
    )

    assert "HISTORY.rst" in out


def test_git_flow_add_specific_file_to_commit(test_environment):
    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["VERSION"]

    VERSION = ['major', 'minor', 'patch']

    VCS = {
        'name': 'git-flow',
        'include_files': ['HISTORY.rst']
    }
    """

    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.ensure_file_is_present("HISTORY.rst")

    test_environment.call(["git", "init"])
    test_environment.call(["git", "flow", "init", "-d"])

    test_environment.call(["git", "add", "punch_config.py"])
    test_environment.call(["git", "add", "punch_version.py"])
    test_environment.call(["git", "add", "VERSION"])

    test_environment.call(["git", "commit", "-m", "Initial version"])

    test_environment.call(["punch", "--part", "minor"])

    out = test_environment.output(
        ["git", "ls-tree", "-r", "master", "--name-only"]
    )

    assert "HISTORY.rst" in out


def test_git_flow_add_all_files_to_commit(test_environment):
    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["VERSION"]

    VERSION = ['major', 'minor', 'patch']

    VCS = {
        'name': 'git-flow',
        'include_all_files': True
    }
    """

    test_environment.ensure_file_is_present("VERSION", "0.2.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    test_environment.ensure_file_is_present("HISTORY.rst")

    test_environment.call(["git", "init"])
    test_environment.call(["git", "flow", "init", "-d"])

    test_environment.call(["git", "add", "punch_config.py"])
    test_environment.call(["git", "add", "punch_version.py"])
    test_environment.call(["git", "add", "VERSION"])

    test_environment.call(["git", "commit", "-m", "Initial version"])

    test_environment.call(["punch", "--part", "minor"])

    out = test_environment.output(
        ["git", "ls-tree", "-r", "master", "--name-only"]
    )

    assert "HISTORY.rst" in out
