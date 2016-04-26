# -*- coding: utf-8 -*-

import pytest

from punch import version as ver
from punch import version_part as vp


@pytest.fixture
def version_mmp():
    v = ver.Version()
    v.add_part('major', 4)
    v.add_part('minor', 3)
    v.add_part('patch', 1)
    return v


def test_version_default_part_is_integer():
    v = ver.Version()
    v.add_part('major', 4)
    assert isinstance(v.get_part('major'), vp.IntegerVersionPart)


def test_version_may_specify_part_class():
    v = ver.Version()
    v.add_part('major', 4, vp.ValueListVersionPart, [0, 2, 4, 6, 8])
    assert isinstance(v.get_part('major'), vp.ValueListVersionPart)
    assert v.get_part('major').value == 4
    assert v.get_part('major').values == [0, 2, 4, 6, 8]


def test_version_can_add_parts(version_mmp):
    assert version_mmp.get_part('major').value == 4


def test_version_increment_last_part(version_mmp):
    version_mmp.inc('patch')
    assert version_mmp.get_part('patch').value == 2


def test_version_increment_minor_part(version_mmp):
    version_mmp.inc('minor')
    assert version_mmp.get_part('minor').value == 4
    assert version_mmp.get_part('patch').value == 0


def test_version_increment_major_part(version_mmp):
    version_mmp.inc('major')
    assert version_mmp.get_part('major').value == 5
    assert version_mmp.get_part('minor').value == 0
    assert version_mmp.get_part('patch').value == 0
