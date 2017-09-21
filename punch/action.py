import sys


def action_type2class(action_type):
    class_name = action_type.title().replace("_", "") + 'Action'
    return getattr(sys.modules[__name__], class_name)


class Action(object):

    @classmethod
    def _action_type2class(cls, action_type):
        class_name = action_type.title().replace("_", "") + 'Action'
        return getattr(sys.modules[__name__], class_name)

    @classmethod
    def from_dict(cls, dic):
        action_type = dic.pop('type')
        action_class = cls._action_type2class(action_type)
        return action_class(**dic)


class ConditionalResetAction:

    def __init__(self, field, update_fields=None, **kwds):
        self.field = field
        self.update_fields = update_fields

    def process_version(self, version):
        new_version = version.copy()

        reset_part = new_version.get_part(self.field)

        for f in self.update_fields:
            update_part = new_version.get_part(f)
            update_part.inc()

        if new_version == version:
            reset_part.inc()
        else:
            reset_part.reset()

        return new_version


class IncreasePartAction:

    def __init__(self, part, **kwds):
        self.part = part

    def process_version(self, version):
        new_version = version.copy()
        new_version.inc(self.part)

        return new_version


class SetPartAction:

    def __init__(self, **kwds):
        self.parts = kwds

    def process_version(self, version):
        new_version = version.copy()
        new_version.set(self.parts)

        return new_version
