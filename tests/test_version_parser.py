# -*- coding: utf-8 -*-

import pytest

from punch import version_parser as vp

def test_parse_version_mmp():
    parser = vp.VersionParser()
    version = parser.parse('5.0.3', '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')

    assert version.get_part('major') == '5'
    assert version.get_part('minor') == '0'
    assert version.get_part('patch') == '3'

def test_parse_version_api_abi():
    parser = vp.VersionParser()
    version = parser.parse('5.0', '(?P<api>\d+)\.(?P<abi>\d+)')

    assert version.get_part('api') == '5'
    assert version.get_part('abi') == '0'

def test_parse_version_no_dots_api_abi():
    parser = vp.VersionParser()
    version = parser.parse('api-5/abi-0', 'api-(?P<api>\d+)\/abi-(?P<abi>\d+)')

    assert version.get_part('api') == '5'
    assert version.get_part('abi') == '0'

def test_parse_error():
    parser = vp.VersionParser()

    with pytest.raises(ValueError):
        parser.parse('5.0', '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')

