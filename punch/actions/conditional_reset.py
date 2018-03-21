from __future__ import print_function, absolute_import, division


class ConditionalResetAction(object):

    def __init__(self, adict):
        self.field = adict['field']
        self.update_fields = adict.get('update_fields', None)

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
