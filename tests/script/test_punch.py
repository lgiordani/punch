import pytest

pytestmark = pytest.mark.slow


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
