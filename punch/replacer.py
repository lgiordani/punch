from __future__ import print_function, absolute_import, division

import six
from collections import abc
from jinja2 import Template

# This class implements the replacement engine in a text
# A Replaces is initialized with serializers, which are Jinja2 templates to
# serialize a version, such as '{{major}}.{{minor}}.{{patch}}'.
# The Replacer.replace method accepts  a text, a current version, and a
# new version. For each serializer, it renders the two versions and replaces
# the first with the second.


class MissingMainSerializer(Exception):
    """A class used to signal that the main serializer is not present.
    Usually this means that the serializers have been given as a dict
    but no main serializer name option has been specified"""
    pass


class Replacer(object):
    def __init__(self, serializers, main_serialize_name='0'):

        # Serializers is a list
        if isinstance(serializers, abc.MutableSequence):
            self.serializers = dict(
                ((str(k), v) for k, v in enumerate(serializers))
            )
        # Serializers is a string
        elif isinstance(serializers, abc.Sequence):
            self.serializers = {
                '0': serializers
            }
        # Serializers is a dictionary
        elif isinstance(serializers, abc.Mapping):
            self.serializers = serializers
        else:
            raise(TypeError(
                ("serializers must be either a MutableSequence, "
                 "a Sequence, or a Mapping.")
            ))

    def run_serializer(self, serializer_name,
                       current_version_dict, new_version_dict):
        template = Template(self.serializers[serializer_name])

        return (
            template.render(**current_version_dict),
            template.render(**new_version_dict)
        )

    def _run_serializer(
            self, serializer, current_version_dict, new_version_dict):
        template = Template(serializer)

        return (
            template.render(**current_version_dict),
            template.render(**new_version_dict)
        )

    def run_all_serializers(self, current_version_dict, new_version_dict):
        """
        Renders all serializers and returns old and new versions.
        This function runs all the provided serializers on the given current
        version, and returns a dictionary where each element is a tuple
        with the current and new version rendered according to the relative
        serializer.
        """

        rendered_templates = {}
        for name, serializer in self.serializers.items():
            rendered_templates[name] = self.run_serializer(
                name, current_version_dict, new_version_dict)

        return rendered_templates

    def run_main_serializer(self, current_version_dict, new_version_dict):
        rendered_templates = {}
        for serializer in [self.main_serializer]:
            template = Template(serializer)

            rendered_templates['main'] = (
                template.render(**current_version_dict),
                template.render(**new_version_dict)
            )

        return rendered_templates['main']

    def replace(self, text, current_version_dict, new_version_dict):
        if six.PY2:
            text = text.decode('utf8')

        templates = self.run_all_serializers(
            current_version_dict,
            new_version_dict
        )

        for name, templates in templates.items():
            text = text.replace(templates[0], templates[1])

        return text
