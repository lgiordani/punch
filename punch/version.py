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
        for key in self.keys[idx+1:]:
            self.parts[key].reset()
