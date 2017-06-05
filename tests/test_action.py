# -*- coding: utf-8 -*-

import pytest

from punch import version as ver
from punch import version_part as vp
from punch import action


def test_conditional_reset_init_with_no_field():
    with pytest.raises(TypeError):
        action.ConditionalResetAction()


def test_conditional_reset_init_field():
    a = action.ConditionalResetAction('a')
    assert a.field == 'a'


def test_conditional_reset_init_field_explicit():
    a = action.ConditionalResetAction(field='a')
    assert a.field == 'a'


def test_conditional_reset_init_accepts_update_fields():
    a = action.ConditionalResetAction(
        field='a', update_fields=['b', 'c'])
    assert a.field == 'a'
    assert a.update_fields == ['b', 'c']


def test_conditional_reset_process_version_checks_all_update_fields(mocker):
    mocker.patch('punch.version_part.DateVersionPart.inc')
    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')
    part_month = vp.DateVersionPart('month', 1, '%m')
    part_build = vp.IntegerVersionPart('build')
    v.add_part(part_year)
    v.add_part(part_month)
    v.add_part(part_build)

    a = action.ConditionalResetAction(
        field='build',
        update_fields=['year', 'month']
    )

    a.process_version(v)

    assert part_year.inc.called
    assert part_month.inc.called


def test_conditional_reset_process_version_calls_reset_on_field(mocker):
    mocker.patch('punch.version_part.IntegerVersionPart.reset')
    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')
    part_month = vp.DateVersionPart('month', 1, '%m')
    part_build = vp.IntegerVersionPart('build')
    v.add_part(part_year)
    v.add_part(part_month)
    v.add_part(part_build)

    a = action.ConditionalResetAction(
        field='build',
        update_fields=['year', 'month']
    )

    a.process_version(v)

    assert part_build.reset.called


def test_conditional_reset_process_version_calls_increment_on_field(mocker):
    mocker.patch('punch.version_part.IntegerVersionPart.inc')
    strftime = mocker.patch('punch.version_part.strftime')
    strftime.return_value = 2016
    v = ver.Version()
    part_year = vp.DateVersionPart('year', 2016, '%Y')
    part_build = vp.IntegerVersionPart('build')
    v.add_part(part_year)
    v.add_part(part_build)

    a = action.ConditionalResetAction(
        field='build',
        update_fields=['year']
    )

    a.process_version(v)

    assert part_build.inc.called
