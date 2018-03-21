from __future__ import print_function, absolute_import, division


class SetPartAction(object):

    def __init__(self, adict):
        self.parts = adict

    def process_version(self, version):
        new_version = version.copy()
        new_version.set(self.parts)

        return new_version
