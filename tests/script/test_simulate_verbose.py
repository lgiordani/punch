import pytest

import punch

pytestmark = pytest.mark.slow

version_file_content = """
major = 1
minor = 0
patch = 0
"""

config_file_content = """
__config_version__ = 1

GLOBALS = {
    'serializer': '{{major}}.{{minor}}.{{patch}}',
}

FILES = ["README.md"]

VERSION = ['major', 'minor', 'patch']
"""


def test_verbose(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    ret = test_environment.call(["punch", "--verbose", "--part", "major"])

    assert test_environment.get_file_content("README.md") == "Version 2.0.0"
    assert not ret.stderr
    assert ret.stdout == """## Punch version {version}

* Current version
major=1
minor=0
patch=0

* New version
major=2
minor=0
patch=0

* Global version updates
  * 1.0.0 -> 2.0.0

Configured files
* README.md:
  * 1.0.0 -> 2.0.0
""".format(version=punch.__version__)


def test_simulate(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    ret = test_environment.call([
        "punch",
        "--simulate",
        "--part",
        "major"
    ])

    assert test_environment.get_file_content("README.md") == "Version 1.0.0"
    assert not ret.stderr
    assert ret.stdout == """## Punch version {version}

* Current version
major=1
minor=0
patch=0

* New version
major=2
minor=0
patch=0

* Global version updates
  * 1.0.0 -> 2.0.0

Configured files
* README.md:
  * 1.0.0 -> 2.0.0
""".format(version=punch.__version__)


def test_simulate_and_verbose(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present(
        "punch_version.py",
        version_file_content
    )

    test_environment.ensure_file_is_present(
        "punch_config.py",
        config_file_content
    )

    ret = test_environment.call([
        "punch",
        "--simulate",
        "--verbose",
        "--part",
        "major"
    ])

    assert test_environment.get_file_content("README.md") == "Version 1.0.0"
    assert not ret.stderr
    assert ret.stdout == """## Punch version {version}

* Current version
major=1
minor=0
patch=0

* New version
major=2
minor=0
patch=0

* Global version updates
  * 1.0.0 -> 2.0.0

Configured files
* README.md:
  * 1.0.0 -> 2.0.0
""".format(version=punch.__version__)
