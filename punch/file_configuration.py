import six
import jinja2

import collections


def _compile_variable(environment, global_variables, value):
    if six.PY2:
        value = value.decode('utf8')

    if not isinstance(value, collections.Mapping):
        template = environment.from_string(value)
        return template.render(GLOBALS=global_variables)
    else:
        new_value = {}
        for k, v in value.items():
            new_value[k] = _compile_variable(
                environment, global_variables, v)
        return new_value


class FileConfiguration(object):

    def __init__(self, filepath, local_variables, global_variables=None):
        self.config = {}
        if global_variables:
            self.config.update(global_variables)

        new_local_variables = {}
        env = jinja2.Environment(undefined=jinja2.DebugUndefined)
        for key, value in local_variables.items():
            new_local_variables[key] = _compile_variable(
                env, global_variables, value)
            # if six.PY2:
            #     value = value.decode('utf8')

            # template = env.from_string(value)
            # new_local_variables[key] = template.render(
            #     GLOBALS=global_variables)

        self.config.update(new_local_variables)
        self.path = filepath

    @classmethod
    def from_dict(cls, dic, global_variables):
        return cls(dic['path'], dic, global_variables)
