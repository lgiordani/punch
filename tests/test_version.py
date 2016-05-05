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
