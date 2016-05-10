# -*- coding: utf-8 -*-

import os
import pytest

from punch import version as ver
from punch import version_part as vp


def clean_previous_imports():
    import sys

    for i in ['punch_config', 'punch_version']:
        if i in sys.modules:
            sys.modules.pop(i)


@pytest.fixture
def version_mmp():
    v = ver.Version()
    v.create_part('major', 4)
    v.create_part('minor', 3)
    v.create_part('patch', 1)
    return v


@pytest.fixture
def version_mmpb():
    v = ver.Version()
    v.create_part('major', 4)
    v.create_part('minor', 3)
    v.create_part('patch', 1)
    v.create_part('build', 5, start_value=1)
    return v


def test_version_default_part_is_integer():
    v = ver.Version()
    v.create_part('major', 4)
    assert isinstance(v.get_part('major'), vp.IntegerVersionPart)


def test_version_add_parts():
    v = ver.Version()
    part_major = vp.IntegerVersionPart('major', 4)
    part_minor = vp.IntegerVersionPart('minor', 3)
    v.add_part(part_major)
    v.add_part(part_minor)

    assert v.get_part('major').value == 4
    assert v.get_part('minor').value == 3
    assert v.keys == ['major', 'minor']


def test_version_may_specify_part_class():
    v = ver.Version()
    v.create_part('major', 4, vp.ValueListVersionPart, [0, 2, 4, 6, 8])
    assert isinstance(v.get_part('major'), vp.ValueListVersionPart)
    assert v.get_part('major').value == 4
    assert v.get_part('major').values == [0, 2, 4, 6, 8]


def test_version_can_add_parts(version_mmp):
    assert version_mmp.get_part('major').value == 4


def test_version_increment_last_part(version_mmp):
    version_mmp.inc('patch')
    assert version_mmp.get_part('patch').value == 2


def test_version_increment_middle_part(version_mmp):
    version_mmp.inc('minor')
    assert version_mmp.get_part('minor').value == 4
    assert version_mmp.get_part('patch').value == 0


def test_version_increment_first_part(version_mmp):
    version_mmp.inc('major')
    assert version_mmp.get_part('major').value == 5
    assert version_mmp.get_part('minor').value == 0
    assert version_mmp.get_part('patch').value == 0


def test_version_increment_part_with_custom_start_value(version_mmpb):
    version_mmpb.inc('major')
    assert version_mmpb.get_part('major').value == 5
    assert version_mmpb.get_part('minor').value == 0
    assert version_mmpb.get_part('patch').value == 0
    assert version_mmpb.get_part('build').value == 1


def test_version_copy(version_mmp):
    new_version = version_mmp.copy()
    new_version.inc('major')
    assert new_version.get_part('major').value == 5
    assert new_version.get_part('minor').value == 0
    assert new_version.get_part('patch').value == 0


def test_version_as_list(version_mmp):
    assert version_mmp.as_list() == [('major', 4), ('minor', 3), ('patch', 1)]


def test_version_keys_and_values(version_mmp):
    assert version_mmp.keys == ['major', 'minor', 'patch']
    assert [i.value for i in version_mmp.values] == [4, 3, 1]


def test_version_keys_keep_indertion_order(version_mmp):
    minor = version_mmp.parts.pop('minor')
    version_mmp.add_part(minor)
    assert version_mmp.as_list() == [('major', 4), ('patch', 1), ('minor', 3)]


def test_version_as_dict(version_mmp):
    expected_dict = {
        'major': 4,
        'minor': 3,
        'patch': 1
    }

    assert version_mmp.as_dict() == expected_dict


def test_write_version_file(temp_empty_dir, version_mmp):
    clean_previous_imports()

    version_filepath = os.path.join(temp_empty_dir, 'punch_version.py')

    version_mmp.to_file(version_filepath)

    with open(version_filepath, 'r') as f:
        content = sorted(f.readlines())

    expected_content = [
        "major = 4\n",
        "minor = 3\n",
        "patch = 1\n"
    ]

    assert content == expected_content


def test_read_complete_version_from_file(temp_empty_dir, version_mmp):
    clean_previous_imports()

    version_filepath = os.path.join(temp_empty_dir, 'punch_version.py')

    with open(version_filepath, 'w') as f:
        f.writelines(["major = 4\n", "minor = 3\n", "patch = 1\n"])

    version_description = [
        {
            'name': 'major',
            'type': 'integer'
        },
        {
            'name': 'minor',
            'type': 'integer'
        },
        {
            'name': 'patch',
            'type': 'integer'
        }
    ]

    version = ver.Version.from_file(version_filepath, version_description)

    assert version.keys == ['major', 'minor', 'patch']
    assert len(version.parts) == 3
    assert version.parts['major'].value == 4
    assert version.parts['minor'].value == 3
    assert version.parts['patch'].value == 1


def test_read_simplified_version_from_file(temp_empty_dir, version_mmp):
    clean_previous_imports()

    version_filepath = os.path.join(temp_empty_dir, 'punch_version.py')

    with open(version_filepath, 'w') as f:
        f.writelines(["major = 4\n", "minor = 3\n", "patch = 1\n"])

    version_description = ['major', 'minor', 'patch']

    version = ver.Version.from_file(version_filepath, version_description)

    assert version.keys == ['major', 'minor', 'patch']
    assert len(version.parts) == 3
    assert version.parts['major'].value == 4
    assert version.parts['minor'].value == 3
    assert version.parts['patch'].value == 1
