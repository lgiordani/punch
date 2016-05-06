from jinja2 import Template

class Replacer:
    def __init__(self, serializer):
        self.serializer = serializer

    def replace(self, text, current_version, new_version):
        template = Template(self.serializer)

        _search_pattern = template.render(**current_version)
        _replace_pattern = template.render(**new_version)

        return text.replace(_search_pattern, _replace_pattern)
