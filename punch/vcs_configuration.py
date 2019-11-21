from __future__ import print_function, absolute_import, division

from collections import abc

from jinja2 import Template


class VCSConfiguration(object):

    def __init__(self, name, options, global_variables, special_variables,
                 commit_message=None, finish_release=True,
                 include_files=None, include_all_files=False):
        self.name = name

        if commit_message is None:
            commit_message = \
                "Version updated {{ current_version }} -> {{ new_version }}"

        commit_message_template = Template(commit_message)

        template_variables = {}
        template_variables.update(global_variables)
        template_variables.update(special_variables)

        self.commit_message = commit_message_template.render(
            **template_variables)
        self.finish_release = finish_release

        self.options = {}
        for key, value in options.items():
            if isinstance(value, abc.Sequence):
                value_template = Template(value)
                self.options[key] = value_template.render(**template_variables)
            else:
                self.options[key] = value

        self.options.update(special_variables)

        self.include_files = include_files or []
        self.include_all_files = include_all_files

    @classmethod
    def from_dict(cls, vcs_configuration_dict,
                  global_variables, special_variables):
        return VCSConfiguration(
            vcs_configuration_dict['name'],
            vcs_configuration_dict.get('options', {}),
            global_variables,
            special_variables,
            vcs_configuration_dict.get(
                'commit_message', None),
            vcs_configuration_dict.get(
                'finish_release', True
            ),
            vcs_configuration_dict.get(
                'include_files', None
            ),
            vcs_configuration_dict.get(
                'include_all_files', False
            )
        )
