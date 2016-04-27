import os

class GlobalConfig:
    def __init__(self):
        self.config = dict(("${}".format(key), value) for key, value in os.environ.items())

    def add_variable(self, key, value):
        self.config[key] = value

    def add_dict(self, other):
        self.config.update(other)

    def format(self, string):
        return string.format(**self.config)