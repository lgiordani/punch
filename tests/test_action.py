# -*- coding: utf-8 -*-

import pytest
from unittest import mock

from punch import version as ver
from punch import version_part as vp
from punch import action


def test_refresh_action_init_with_no_refresh_fields():
    with pytest.raises(TypeError):
        action.RefreshAction()


def test_refresh_action_init_refresh_fields():
    a = action.RefreshAction(['a', 'b'])
    assert a.refresh_fields == ['a', 'b']


def test_refresh_action_init_refresh_fields_explicitly():
    a = action.RefreshAction(refresh_fields=['a', 'b'])
    assert a.refresh_fields == ['a', 'b']


def test_refresh_action_init_accepts_fallback():
    a = action.RefreshAction(
        refresh_fields=['a', 'b'], fallback_field='fallback_field')
    assert a.refresh_fields == ['a', 'b']
    assert a.fallback_field == 'fallback_field'


def test_refresh_action_process_version_checks_for_date_fields(
        mocker):
    mocker.patch('punch.action.vp.DateVersionPart.inc')
    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')
    v.add_part(part_year)

    a = action.RefreshAction(
        refresh_fields=['year']
    )

    a.process_version(v)

    assert part_year.inc.called


def test_refresh_action_process_version_requires_date_version_parts():
    v = ver.Version()
    part_year = vp.IntegerVersionPart('year', 2016, 0)
    v.add_part(part_year)

    a = action.RefreshAction(
        refresh_fields=['year']
    )

    with pytest.raises(TypeError):
        a.process_version(v)


def test_refresh_action_process_version_checks_multiple_fields(mocker):
    mocker.patch('punch.action.vp.DateVersionPart.inc')
    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')
    part_month = vp.DateVersionPart('month', 1, '%m')
    v.add_part(part_year)
    v.add_part(part_month)

    a = action.RefreshAction(
        refresh_fields=['year', 'month']
    )

    a.process_version(v)

    assert part_year.inc.called
    assert part_month.inc.called


def test_refresh_action_process_version_uses_fallback_field(mocker):
    mock_dateversionpart_inc = mocker.patch(
        'punch.action.vp.IntegerVersionPart.inc')
    mocker.patch('punch.action.vp.DateVersionPart.inc')

    # This makes the inc() function act as a NOP
    mock_dateversionpart_inc.inc.side_effect = lambda x: None

    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')
    part_month = vp.DateVersionPart('month', 1, '%m')
    part_build = vp.IntegerVersionPart('build', 0, 0)

    v.add_part(part_year)
    v.add_part(part_month)
    v.add_part(part_build)

    a = action.RefreshAction(
        refresh_fields=['year', 'month'],
        fallback_field='build'
    )

    a.process_version(v)

    assert part_year.inc.called
    assert part_month.inc.called
    assert part_build.inc.called


def test_refresh_action_process_version_skips_fallback_field_if_refresh_works(
        mocker):

    mocker.patch('punch.action.vp.IntegerVersionPart.inc')
    mock_strftime = mocker.patch('punch.action.vp.strftime')
    mock_strftime.return_value = 42

    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')
    part_month = vp.DateVersionPart('month', 1, '%m')
    part_build = vp.IntegerVersionPart('build', 0, 0)

    v.add_part(part_year)
    v.add_part(part_month)
    v.add_part(part_build)

    a = action.RefreshAction(
        refresh_fields=['year', 'month'],
        fallback_field='build'
    )

    a.process_version(v)

    assert not part_build.inc.called


def test_refresh_action_process_version_returns_new_version(mocker):

    mock_strftime = mocker.patch('punch.action.vp.strftime')
    mock_strftime.return_value = 1234

    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')

    v.add_part(part_year)

    a = action.RefreshAction(
        refresh_fields=['year']
    )

    new_version = a.process_version(v)

    assert new_version.as_dict() == {'year': 1234}


def test_get_refresh_action_from_dict():
    input_dict = {
        'type': 'refresh',
        'refresh_fields': ['year', 'month'],
        'fallback_field': 'build'
    }

    act = action.Action.from_dict(input_dict)

    assert act.refresh_fields == ['year', 'month']
    assert act.fallback_field == 'build'
    assert isinstance(act, action.RefreshAction)
