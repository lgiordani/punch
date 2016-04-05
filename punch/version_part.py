# -*- coding: utf-8 -*-

class IntegerVersionPart():
    def __init__(self, value):
        self.value = value

    def inc(self):
        self.value = self.value + 1

    def reset(self):
        self.value = 0