import collections

from jinja2 import Template


class VCSConfiguration(object):
    def __init__(self, name, commit_message, options, global_variables, special_variables):
        self.name = name

        commit_message_template = Template(commit_message)

        template_variables = {}
        template_variables.update(global_variables)
        template_variables.update(special_variables)

        self.commit_message = commit_message_template.render(**template_variables)

        self.options = {}
        for key, value in options.items():
            if isinstance(value, collections.Sequence):
                value_template = Template(value)
                self.options[key] = value_template.render(**template_variables)
            else:
                self.options[key] = value

    @classmethod
    def from_dict(cls, vcs_configuration_dict, global_variables, special_variables):
        return VCSConfiguration(vcs_configuration_dict['name'],
                                vcs_configuration_dict['commit_message'],
                                vcs_configuration_dict['options'],
                                global_variables,
                                special_variables)
