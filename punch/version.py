# -*- coding: utf-8 -*-

from punch import version_part as vpart


class Version():
    def __init__(self):
        self.keys = []
        self.parts = {}

    def add_part(self, name, value, cls=vpart.IntegerVersionPart, *args, **kwds):
        self.keys.append(name)
        self.parts[name] = cls(name, value, *args, **kwds)

    def add_part_from_dict(self, dic):
        vp = vpart.VersionPart.from_dict(dic)
        self.keys.append(vp.name)
        self.parts[vp.name] = vp

    def get_part(self, name):
        return self.parts[name]

    def inc(self, name):
        self.parts[name].inc()
        idx = self.keys.index(name)
        for key in self.keys[idx + 1:]:
            self.parts[key].reset()

    def as_dict(self):
        return dict((key, part.value) for key, part in self.parts.items())

    def to_file(self, version_filepath):
        with open(version_filepath, 'w') as f:
            for key in self.keys:
                f.write("{0} = {1}\n".format(key, self.parts[key].value))
