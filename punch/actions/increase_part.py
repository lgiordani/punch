from __future__ import print_function, absolute_import, division


class IncreasePartAction(object):

    def __init__(self, adict):
        self.part = adict['part']

    def process_version(self, version):
        new_version = version.copy()
        new_version.inc(self.part)

        return new_version
