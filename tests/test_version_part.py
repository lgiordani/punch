# -*- coding: utf-8 -*-

import pytest

from punch import version_part as vpart


def test_integer_version_part_init_with_integer():
    vp = vpart.IntegerVersionPart(4)
    assert vp.value == 4

def test_integer_version_part_init_with_string():
    vp = vpart.IntegerVersionPart('4')
    assert vp.value == 4

def test_integer_version_part_init_with_none():
    vp = vpart.IntegerVersionPart(None)
    assert vp.value == 0


def test_integer_version_part_increases():
    vp = vpart.IntegerVersionPart(4)
    vp.inc()
    assert vp.value == 5


def test_integer_version_part_reset():
    vp = vpart.IntegerVersionPart(4)
    vp.reset()
    assert vp.value == 0


def test_valuelist_version_part_init_with_allowed_value():
    vp = vpart.ValueListVersionPart(0, [0, 2, 4, 6, 8])
    assert vp.value == 0


def test_valuelist_version_part_init_with_not_allowed_value():
    with pytest.raises(ValueError):
        vpart.ValueListVersionPart(1, [0, 2, 4, 6, 8])


def test_valuelist_version_part_init_with_none():
    vp = vpart.ValueListVersionPart(None, [0, 2, 4, 6, 8])
    assert vp.value == 0


def test_valuelist_version_part_increase():
    vp = vpart.ValueListVersionPart(0, [0, 2, 4, 6, 8])
    vp.inc()
    assert vp.value == 2

def test_valuelist_version_part_increase_from_last():
    vp = vpart.ValueListVersionPart(8, [0, 2, 4, 6, 8])
    vp.inc()
    assert vp.value == 0


def test_valuelist_version_part_increase_with_non_numerical_values():
    vp = vpart.ValueListVersionPart(0, [0, 'alpha', 'beta', 'rc1', 'rc2', 1])
    vp.inc()
    assert vp.value == 'alpha'

def test_valuelist_version_part_reset():
    vp = vpart.ValueListVersionPart(4, [0, 2, 4, 6, 8])
    vp.reset()
    assert vp.value == 0
