import sys


class Action(object):

    @classmethod
    def from_dict(cls, dic):
        action_type = dic.pop('type')

        class_name = action_type.title().replace("_", "") + 'Action'
        action_class = getattr(sys.modules[__name__], class_name)

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
