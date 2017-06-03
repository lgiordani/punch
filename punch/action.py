import sys

from punch import version_part as vp


class Action(object):

    @classmethod
    def from_dict(cls, dic):
        action_type = dic.pop('type')

        class_name = action_type.title().replace("_", "") + 'Action'
        action_class = getattr(sys.modules[__name__], class_name)

        return action_class(**dic)


class RefreshAction:

    def __init__(self, refresh_fields, fallback_field=None, **kwds):
        self.refresh_fields = refresh_fields
        self.fallback_field = fallback_field

    def process_version(self, version):
        new_version = version.copy()

        for field in self.refresh_fields:
            part = new_version.get_part(field)
            if not isinstance(part, vp.DateVersionPart):
                raise TypeError
            part.inc()

        print(version.as_dict(), new_version.as_dict())

        if new_version == version and self.fallback_field:
            fallback_part = new_version.get_part(self.fallback_field)
            fallback_part.inc()

        return new_version
