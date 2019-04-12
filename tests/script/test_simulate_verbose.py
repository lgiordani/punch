import pytest

import punch

pytestmark = pytest.mark.slow

version_file_content = """
major = 1
minor = 0
patch = 0
"""

config_file_content_without_vcs = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']
"""


config_file_content_with_git = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git'
}
"""


config_file_content_with_git_flow = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'git-flow'
}
"""

config_file_content_with_hg = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']

VCS = {
    'name': 'hg'
}
"""


@pytest.fixture
def verbose_output_without_vcs():
    return """## Punch version {version}

# Current version
major=1
minor=0
patch=0

# New version
major=2
minor=0
patch=0

# Global version updates
  - 1.0.0 -> 2.0.0

# Configured files
+ README.md:
  - 1.0.0 -> 2.0.0
"""


@pytest.fixture
def verbose_output_with_git(verbose_output_without_vcs):
    return verbose_output_without_vcs + """
# VCS
+ Commit message: {commit_message}
+ Create release branch: yes
+ Release branch: 2.0.0
+ Annotate tags: no
+ Annotation message: 
"""


@pytest.fixture
def verbose_output_with_git_flow(verbose_output_without_vcs):
    return verbose_output_without_vcs + """
# VCS
+ Commit message: {commit_message}
+ Release branch: release/2.0.0
"""


@pytest.fixture
def verbose_output_with_hg(verbose_output_without_vcs):
    return verbose_output_without_vcs + """
# VCS
+ Commit message: {commit_message}
"""


def test_verbose(test_environment, verbose_output_without_vcs):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_without_vcs
    )

    ret = test_environment.call(["punch", "--verbose", "--part", "major"])

    assert not ret.stderr
    assert ret.stdout == verbose_output_without_vcs.format(
        version=punch.__version__
    )
    assert test_environment.get_file_content("README.md") == "Version 2.0.0"


def test_simulate(test_environment, verbose_output_without_vcs):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_without_vcs
    )

    ret = test_environment.call([
        "punch",
        "--simulate",
        "--part",
        "major"
    ])

    assert not ret.stderr
    assert ret.stdout == verbose_output_without_vcs.format(
        version=punch.__version__
    )
    assert test_environment.get_file_content("README.md") == "Version 1.0.0"


def test_simulate_and_verbose(test_environment, verbose_output_without_vcs):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_without_vcs
    )

    ret = test_environment.call([
        "punch",
        "--simulate",
        "--verbose",
        "--part",
        "major"
    ])

    assert not ret.stderr
    assert ret.stdout == verbose_output_without_vcs.format(
        version=punch.__version__
    )
    assert test_environment.get_file_content("README.md") == "Version 1.0.0"


def test_simulate_with_git(test_environment, verbose_output_with_git):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_with_git
    )

    test_environment.output(["git", "init"])

    ret = test_environment.call([
        "punch",
        "--simulate",
        "--part",
        "major"
    ])

    assert not ret.stderr
    assert ret.stdout == verbose_output_with_git.format(
        version=punch.__version__,
        commit_message="Version updated 1.0.0 -> 2.0.0"
    )
    assert test_environment.get_file_content("README.md") == "Version 1.0.0"


def test_simulate_with_git_flow(test_environment, verbose_output_with_git_flow):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_with_git_flow
    )

    test_environment.output(["git", "init"])
    test_environment.output(["git", "flow", "init", "-d"])

    ret = test_environment.call([
        "punch",
        "--simulate",
        "--part",
        "major"
    ])

    assert not ret.stderr
    assert ret.stdout == verbose_output_with_git_flow.format(
        version=punch.__version__,
        commit_message="Version updated 1.0.0 -> 2.0.0"
    )
    assert test_environment.get_file_content("README.md") == "Version 1.0.0"


def test_simulate_with_hg(test_environment, verbose_output_with_hg):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content_with_hg
    )

    test_environment.output(["hg", "init"])

    ret = test_environment.call([
        "punch",
        "--simulate",
        "--part",
        "major"
    ])

    assert not ret.stderr
    assert ret.stdout == verbose_output_with_hg.format(
        version=punch.__version__,
        commit_message="Version updated 1.0.0 -> 2.0.0"
    )
    assert test_environment.get_file_content("README.md") == "Version 1.0.0"
