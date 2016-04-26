# -*- coding: utf-8 -*-

import pytest

from punch import version_parser as vpars
from punch import version_part as vpart


def test_default_parser_config_uses_integer_parts():
    parser = vpars.VersionParser()
    version = parser.parse('5', '(?P<major>\d+)')

    assert version.get_part('major').value == 5
    assert isinstance(version.get_part('major'), vpart.IntegerVersionPart)


def test_default_parser_config_may_specify_part_class_integer():
    parser = vpars.VersionParser({'major': {'type': 'integer'}})
    version = parser.parse('5', '(?P<major>\d+)')

    assert version.get_part('major').value == 5
    assert isinstance(version.get_part('major'), vpart.IntegerVersionPart)


def test_default_parser_config_may_specify_part_class_value_list():
    config = {
        'major': {
            'type': 'value_list',
            'allowed_values': ['alpha', 'beta', 'gamma']
        }
    }

    parser = vpars.VersionParser(config)
    version = parser.parse('alpha', '(?P<major>\w+)')

    assert version.get_part('major').value == 'alpha'
    assert version.get_part('major').values == ['alpha', 'beta', 'gamma']
    assert isinstance(version.get_part('major'), vpart.ValueListVersionPart)


def test_parse_version_mmp():
    parser = vpars.VersionParser()
    version = parser.parse('5.0.3', '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')

    assert version.get_part('major').value == 5
    assert version.get_part('minor').value == 0
    assert version.get_part('patch').value == 3


def test_parse_version_api_abi():
    parser = vpars.VersionParser()
    version = parser.parse('5.0', '(?P<api>\d+)\.(?P<abi>\d+)')

    assert version.get_part('api').value == 5
    assert version.get_part('abi').value == 0


def test_parse_version_no_dots_api_abi():
    parser = vpars.VersionParser()
    version = parser.parse('api-5/abi-0', 'api-(?P<api>\d+)\/abi-(?P<abi>\d+)')

    assert version.get_part('api').value == 5
    assert version.get_part('abi').value == 0


def test_parse_error():
    parser = vpars.VersionParser()

    with pytest.raises(ValueError):
        parser.parse('5.0', '(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)')


def test_parse_mixed_classes():
    config = {
        'minor': {
            'type': 'value_list',
            'allowed_values': ['alpha', 'beta', 'rc1']
        }
    }

    parser = vpars.VersionParser(config)
    version = parser.parse('5.alpha', '(?P<major>\d+)\.(?P<minor>\w+)')

    assert version.get_part('major').value == 5
    assert isinstance(version.get_part('major'), vpart.IntegerVersionPart)

    assert version.get_part('minor').value == 'alpha'
    assert version.get_part('minor').values == ['alpha', 'beta', 'rc1']
    assert isinstance(version.get_part('minor'), vpart.ValueListVersionPart)


def test_parse_optional_part_present():
    parser = vpars.VersionParser()
    version = parser.parse('5.0', '(?P<api>\d+)(\.(?P<abi>\d+))?')

    assert version.get_part('api').value == 5
    assert version.get_part('abi').value == 0


def test_parse_optional_part_not_present():
    parser = vpars.VersionParser()
    version = parser.parse('5', '(?P<api>\d+)(\.(?P<abi>\d+))?')

    assert version.get_part('api').value == 5
    assert version.get_part('abi').value == 0

def test_parse_optional_part_not_present_with_config():
    config = {
        'abi': {
            'type': 'value_list',
            'allowed_values': ['alpha', 'beta', 'rc1']
        }
    }
    parser = vpars.VersionParser(config)
    version = parser.parse('5', '(?P<api>\d+)(\.(?P<abi>\d+))?')

    assert version.get_part('api').value == 5
    assert version.get_part('abi').value == 'alpha'
