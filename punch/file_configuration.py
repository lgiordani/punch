import jinja2


class FileConfiguration(object):
    def __init__(self, filepath, local_variables, global_variables=None):
        self.config = {}
        if global_variables:
            self.config.update(global_variables)

        new_local_variables = {}
        env = jinja2.Environment(undefined=jinja2.DebugUndefined)
        for key, value in local_variables.items():
            template = env.from_string(value)
            new_local_variables[key] = template.render(GLOBALS=global_variables)

        self.config.update(new_local_variables)
        self.path = filepath

    @classmethod
    def from_dict(cls, dic, global_variables):
        return cls(dic['path'], dic, global_variables)
