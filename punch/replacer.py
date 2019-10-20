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


class Replacer(object):
    def __init__(self, serializers):

        if isinstance(serializers, abc.MutableSequence):
            self.serializers = serializers
        else:
            self.serializers = [serializers]

    def _run_serializer(
            self, serializer, current_version_dict, new_version_dict):
        template = Template(serializer)

        return (
            template.render(**current_version_dict),
            template.render(**new_version_dict)
        )

    def run_all_serializers(self, current_version_dict, new_version_dict):
        summary = []
        for serializer in self.serializers:
            summary.append(
                self._run_serializer(
                    serializer, current_version_dict, new_version_dict
                )
            )

        return summary

    def run_first_serializer(self, current_version_dict, new_version_dict):
        return self._run_serializer(
            self.serializers[0],
            current_version_dict,
            new_version_dict
        )

    def replace(self, text, current_version, new_version):
        if six.PY2:
            text = text.decode('utf8')

        new_text = text
        for serializer in self.serializers:
            template = Template(serializer)

            _search_pattern = template.render(**current_version)
            _replace_pattern = template.render(**new_version)

            new_text = new_text.replace(_search_pattern, _replace_pattern)

        return new_text
