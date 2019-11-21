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


class MissingSerializer(Exception):
    """A class used to signal that the requested serializer is not present.
    Usually this means that the serializers have been given as a dict
    but no main serializer name option has been specified"""
    pass


class Replacer(object):
    def __init__(self, serializers, main_serialize_name='0'):
        self.serializers = {}
        self.update(serializers)

    def update(self, serializers):
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
            self.serializers.update(serializers)
        else:
            raise(TypeError(
                ("serializers must be either a MutableSequence, "
                 "a Sequence, or a Mapping.")
            ))

    def run_serializer(self, serializer_name,
                       current_version_dict, new_version_dict):
        try:
            serializer = self.serializers[serializer_name]
        except KeyError:
            raise MissingSerializer

        if isinstance(serializer, abc.Sequence):
            search_template = Template(serializer)
            replace_template = search_template
        else:
            search_template = Template(serializer['search'])
            replace_template = Template(serializer['replace'])

        return (
            search_template.render(**current_version_dict),
            replace_template.render(**new_version_dict)
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

    def replace(self, text, current_version_dict, new_version_dict):
        if six.PY2:
            text = text.decode('utf8')  # pragma: nocover

        templates = self.run_all_serializers(
            current_version_dict,
            new_version_dict
        )

        for name, templates in templates.items():
            text = text.replace(templates[0], templates[1])

        return text
