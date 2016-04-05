# -*- coding: utf-8 -*-

from punch import version_part as vpart

def test_integer_version_part_increases():
    vp = vpart.IntegerVersionPart(4)
    vp.inc()
    assert vp.value == 5

def test_integer_version_part_reset():
    vp = vpart.IntegerVersionPart(4)
    vp.reset()
    assert vp.value == 0

