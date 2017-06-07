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


def test_integer_version_part_set():
    vp = vpart.IntegerVersionPart('major', 4)
    vp.set(9)
    assert vp.value == 9


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


def test_valuelist_version_part_set():
    vp = vpart.ValueListVersionPart('major', 0, [0, 2, 4, 6, 8])
    vp.set(8)
    assert vp.value == 8


def test_valuelist_version_part_increase_from_last():
    vp = vpart.ValueListVersionPart('major', 8, [0, 2, 4, 6, 8])
    vp.inc()
    assert vp.value == 0


def test_valuelist_version_part_increase_with_non_numerical_values():
    vp = vpart.ValueListVersionPart(
        'major', 0, [0, 'alpha', 'beta', 'rc1', 'rc2', 1]
    )
    vp.inc()
    assert vp.value == 'alpha'


def test_valuelist_version_part_set_with_non_numerical_values():
    vp = vpart.ValueListVersionPart(
        'major', 0, [0, 'alpha', 'beta', 'rc1', 'rc2', 1]
    )
    vp.set('rc1')
    assert vp.value == 'rc1'


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


def test_date_version_part_init_without_value(mocker):
    mock_strftime = mocker.patch('punch.version_part.strftime')
    mock_strftime.return_value = '2018'
    vp = vpart.DateVersionPart('major', value=None, fmt='%Y')
    mock_strftime.assert_called_with('%Y')
    assert vp.value == '2018'


def test_date_version_part_init_with_value(mocker):
    mock_strftime = mocker.patch('punch.version_part.strftime')
    mock_strftime.return_value = '2018'
    vp = vpart.DateVersionPart('major', value='2017', fmt='%Y')
    mock_strftime.assert_not_called()
    assert vp.value == '2017'


def test_date_version_part_reset(mocker):
    mock_strftime = mocker.patch('punch.version_part.strftime')
    vp = vpart.DateVersionPart('major', value='2017', fmt='%Y')
    assert vp.value == '2017'
    mock_strftime.return_value = '2018'
    vp.reset()
    mock_strftime.assert_called_with('%Y')
    assert vp.value == '2018'


def test_date_version_part_increases_just_resets(mocker):
    mock_strftime = mocker.patch('punch.version_part.strftime')
    vp = vpart.DateVersionPart('major', value='2017', fmt='%Y')
    assert vp.value == '2017'
    mock_strftime.return_value = '2018'
    vp.inc()
    mock_strftime.assert_called_with('%Y')
    assert vp.value == '2018'


def test_date_version_part_copy():
    vp = vpart.DateVersionPart('major', value='2017', fmt='%Y%m')
    nvp = vp.copy()

    assert nvp.fmt == '%Y%m'


def test_strftime_full_year(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    vpart.strftime('YYYY')
    mock_strftime.assert_called_with('%Y')


def test_strftime_short_year(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    vpart.strftime('YY')
    mock_strftime.assert_called_with('%y')


def test_strftime_short_year_is_not_padded(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    mock_strftime.return_value = '03'
    assert vpart.strftime('YY') == '3'


def test_strftime_short_month(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    vpart.strftime('MM')
    mock_strftime.assert_called_with('%m')


def test_strftime_short_month_is_not_padded(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    mock_strftime.return_value = '04'
    assert vpart.strftime('MM') == '4'


def test_strftime_zero_padded_short_month(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    vpart.strftime('0M')
    mock_strftime.assert_called_with('%m')


def test_strftime_zero_padded_short_month_is_padded(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    mock_strftime.return_value = '04'
    assert vpart.strftime('0M') == '04'


def test_strftime_short_day(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    vpart.strftime('DD')
    mock_strftime.assert_called_with('%d')


def test_strftime_short_day_is_not_padded(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    mock_strftime.return_value = '04'
    assert vpart.strftime('DD') == '4'


def test_strftime_zero_padded_short_day(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    vpart.strftime('0D')
    mock_strftime.assert_called_with('%d')


def test_strftime_zero_padded_short_day_is_padded(mocker):
    mock_strftime = mocker.patch('punch.version_part._strftime')
    mock_strftime.return_value = '04'
    assert vpart.strftime('0D') == '04'
