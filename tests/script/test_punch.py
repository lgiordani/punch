def test_punch_version_flag(test_environment):
    # output = test_environment_fixture.output(["punch", "--version"])

    # Punch version 1.0.1
    # Copyright (C) 2016 Leonardo Giordani

    expected_output = """
    Copyright \(C\) \d{4} Leonardo Giordani
    This is free software, see the LICENSE file.
    Source: https://github.com/lgiordani/punch
    Documentation: http://punch.readthedocs.io/en/latest/
    """

    test_environment.compare_output(expected_output, ["punch", "--version"])


def test_punch_version_part_without_vcs(test_environment):
    test_environment.ensure_file_is_present("README.md", "Version 1.0.0")

    test_environment.ensure_file_is_present("punch_version.py",
                                                    "major = 1\nminor = 0\npatch = 0\n")

    config_file_content = """
    __config_version__ = 1

    GLOBALS = {
        'serializer': '{{major}}.{{minor}}.{{patch}}',
    }

    FILES = ["README.md"]

    VERSION = ['major', 'minor', 'patch']
    """

    test_environment.ensure_file_is_present("punch_config.py", config_file_content)

    test_environment.call(["punch", "--part", "major"])

    assert test_environment.get_file_content("README.md") == "Version 2.0.0"
