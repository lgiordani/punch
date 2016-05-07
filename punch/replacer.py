import collections
from jinja2 import Template

class Replacer:
    def __init__(self, serializers):

        if isinstance(serializers, collections.MutableSequence):
            self.serializers = serializers
        else:
            self.serializers = [serializers]

    def replace(self, text, current_version, new_version):
        new_text = text
        for serializer in self.serializers:
            template = Template(serializer)

            _search_pattern = template.render(**current_version)
            _replace_pattern = template.render(**new_version)

            new_text = new_text.replace(_search_pattern, _replace_pattern)

        return new_text
