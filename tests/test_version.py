# -*- coding: utf-8 -*-

import pytest

from punch import version as ver


@pytest.fixture
def version_mmp():
    v = ver.Version()
    v.add_part('major', 4)
    v.add_part('minor', 3)
    v.add_part('patch', 1)
    return v


def test_version_can_add_parts(version_mmp):
    assert version_mmp.get_part('major') == 4


def test_version_increment_last_part(version_mmp):
    version_mmp.inc('patch')
    assert version_mmp.get_part('patch') == 2


def test_version_increment_minor_part(version_mmp):
    version_mmp.inc('minor')
    assert version_mmp.get_part('minor') == 4
    assert version_mmp.get_part('patch') == 0

def test_version_increment_major_part(version_mmp):
    version_mmp.inc('major')
    assert version_mmp.get_part('major') == 5
    assert version_mmp.get_part('minor') == 0
    assert version_mmp.get_part('patch') == 0
