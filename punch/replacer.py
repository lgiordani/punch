from __future__ import print_function, absolute_import, division

import six
from collections import abc
from jinja2 import Template


class Replacer(object):
    def __init__(self, serializers):

        if isinstance(serializers, abc.MutableSequence):
            self.serializers = serializers
        else:
            self.serializers = [serializers]

    def run_all_serializers(self, current_version_dict, new_version_dict):
        summary = []
        for serializer in self.serializers:
            template = Template(serializer)

            summary.append((
                template.render(**current_version_dict),
                template.render(**new_version_dict)
            ))

        return summary

    def run_main_serializer(self, current_version_dict, new_version_dict):
        return self.run_all_serializers(
            current_version_dict,
            new_version_dict
        )[0]

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
