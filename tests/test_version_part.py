# -*- coding: utf-8 -*-

import pytest

from punch import version_part as vpart


def test_integer_version_part_init_with_integer():
    vp = vpart.IntegerVersionPart('major', 4)
    assert vp.value == 4


def test_integer_version_part_init_with_string():
    vp = vpart.IntegerVersionPart('major', '4')
    assert vp.value == 4


def test_integer_version_part_init_with_none():
    vp = vpart.IntegerVersionPart('major', None)
    assert vp.value == 0


def test_integer_version_part_init_without_value():
    vp = vpart.IntegerVersionPart('major')
    assert vp.value == 0


def test_integer_version_part_init_with_start_value():
    vp = vpart.IntegerVersionPart('major', start_value=1)
    assert vp.value == 1
    vp.inc()
    vp.reset()
    assert vp.value == 1


def test_integer_version_part_increases():
    vp = vpart.IntegerVersionPart('major', 4)
    vp.inc()
    assert vp.value == 5


def test_integer_version_part_reset():
    vp = vpart.IntegerVersionPart('major', 4)
    vp.reset()
    assert vp.value == 0


def test_integer_version_part_copy():
    vp = vpart.IntegerVersionPart('major', 4)
    nvp = vp.copy()
    vp.inc()

    assert nvp.value == 4


def test_integer_version_part_with_start_value_copy():
    vp = vpart.IntegerVersionPart('major', 4, start_value=1)
    nvp = vp.copy()

    assert nvp.start_value == 1


def test_valuelist_version_part_init_with_allowed_value():
    vp = vpart.ValueListVersionPart('major', 0, [0, 2, 4, 6, 8])
    assert vp.value == 0


def test_valuelist_version_part_init_with_not_allowed_value():
    with pytest.raises(ValueError):
        vpart.ValueListVersionPart('major', 1, [0, 2, 4, 6, 8])


def test_valuelist_version_part_init_with_none():
    vp = vpart.ValueListVersionPart('major', None, [0, 2, 4, 6, 8])
    assert vp.value == 0


def test_valuelist_version_part_increase():
    vp = vpart.ValueListVersionPart('major', 0, [0, 2, 4, 6, 8])
    vp.inc()
    assert vp.value == 2


def test_valuelist_version_part_increase_from_last():
    vp = vpart.ValueListVersionPart('major', 8, [0, 2, 4, 6, 8])
    vp.inc()
    assert vp.value == 0


def test_valuelist_version_part_increase_with_non_numerical_values():
    vp = vpart.ValueListVersionPart('major', 0, [0, 'alpha', 'beta', 'rc1', 'rc2', 1])
    vp.inc()
    assert vp.value == 'alpha'


def test_valuelist_version_part_reset():
    vp = vpart.ValueListVersionPart('major', 4, [0, 2, 4, 6, 8])
    vp.reset()
    assert vp.value == 0


def test_valuelist_version_part_copy():
    vp = vpart.ValueListVersionPart('major', 4, [0, 2, 4, 6, 8])
    nvp = vp.copy()
    vp.inc()
    vp.values.append(9)

    assert nvp.value == 4
    assert nvp.values == [0, 2, 4, 6, 8]


def test_get_integer_version_part_from_full_dict():
    input_dict = {
        'name': 'major',
        'value': 1,
        'type': 'integer'
    }

    vp = vpart.VersionPart.from_dict(input_dict)

    assert vp.name == 'major'
    assert vp.value == 1
    assert isinstance(vp, vpart.IntegerVersionPart)


def test_get_integer_version_part_from_partial_dict():
    input_dict = {
        'name': 'major',
        'value': 1,
    }

    vp = vpart.VersionPart.from_dict(input_dict)

    assert vp.name == 'major'
    assert vp.value == 1
    assert isinstance(vp, vpart.IntegerVersionPart)


def test_get_value_list_version_part_from_full_dict():
    input_dict = {
        'name': 'major',
        'value': 'alpha',
        'type': 'value_list',
        'allowed_values': ['alpha', 'beta', 'stable']
    }

    vp = vpart.VersionPart.from_dict(input_dict)

    assert vp.name == 'major'
    assert vp.value == 'alpha'
    assert isinstance(vp, vpart.ValueListVersionPart)
    assert vp.values == ['alpha', 'beta', 'stable']
