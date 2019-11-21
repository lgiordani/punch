from __future__ import print_function, absolute_import, division


class FileConfiguration(object):

    def __init__(self, filepath, local_variables, global_variables=None):
        self.config = {}
        if global_variables:
            self.config.update(global_variables)

        self.config.update(local_variables)
        self.path = filepath

    @classmethod
    def from_dict(cls, dic, global_variables):
        return cls(dic['path'], dic, global_variables)
