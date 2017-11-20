# -*- coding: utf-8 -*-

from punch import action_register


def test_action_resgister():
    class ASimpleTestAction(object):
        pass

    action_register.ActionRegister.register(ASimpleTestAction, 'a_simple_test')

    assert action_register.ActionRegister.get(
        'a_simple_test') == ASimpleTestAction
