# import pytest

from punch import helpers


def test_optstr2dict_single_option():
    optstr = "part=major"

    assert helpers.optstr2dict(optstr) == {
        'part': 'major'
    }


def test_optstr2dict_multiple_options():
    optstr = "part=major,reset=true"

    assert helpers.optstr2dict(optstr) == {
        'part': 'major',
        'reset': 'true'
    }


def test_optstr2dict_convert_boolean():
    optstr = "reset=true"

    assert helpers.optstr2dict(optstr, convert_boolean=True) == {
        'reset': True
    }


def test_optstr2dict_convert_boolean_false():
    optstr = "reset=false"

    assert helpers.optstr2dict(optstr, convert_boolean=True) == {
        'reset': False
    }


def test_optstr2dict_convert_boolean_mixed_case():
    optstr = "reset=TrUe"

    assert helpers.optstr2dict(optstr, convert_boolean=True) == {
        'reset': True
    }
