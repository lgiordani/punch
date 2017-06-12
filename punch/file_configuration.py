import six
import jinja2

import collections


class FileConfiguration(object):
    def __init__(self, filepath, local_variables, global_variables=None):
        self.config = {}
        if global_variables:
            self.config.update(global_variables)

        new_local_variables = {}
        env = jinja2.Environment(undefined=jinja2.DebugUndefined)

        # TODO: is there a better way?
        for key, value in local_variables.items():
            if six.PY2:
                value = value.decode('utf8')

            # TODO this limits the use of GLOBALS in nested local variables
            if not isinstance(value, collections.Mapping):
                template = env.from_string(value)
                new_local_variables[key] = template.render(
                    GLOBALS=global_variables)

        self.config.update(new_local_variables)
        self.path = filepath

        # Backward compatibility with previous syntax
        if 'serializer' in self.config and 'strategy' not in self.config:
            self.config['strategy'] = {
                'type': 'replace',
                'serializers': [self.config['serializer']]
            }

            self.config.pop('serializer')

    @classmethod
    def from_dict(cls, dic, global_variables):
        return cls(dic['path'], dic, global_variables)
