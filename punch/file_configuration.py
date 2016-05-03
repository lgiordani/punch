class FileConfiguration(object):
    def __init__(self, filepath, variables):
        for var, value in variables.items():
            setattr(self, var, value)
        self.path = filepath
