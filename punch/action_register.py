from __future__ import print_function, absolute_import, division

from punch.actions import increase_part
from punch.actions import set_part
from punch.actions import conditional_reset


class ActionRegister(object):
    _register = {}

    @classmethod
    def register(cls, aclass, class_name):
        cls._register[class_name] = aclass

    @classmethod
    def get(cls, action_name):
        return cls._register[action_name]


ActionRegister.register(increase_part.IncreasePartAction, 'increase_part')
ActionRegister.register(set_part.SetPartAction, 'set_part')
ActionRegister.register(
    conditional_reset.ConditionalResetAction, 'conditional_reset'
)
