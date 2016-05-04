import mock


class Replacer:
    def __init__(self, serializer):
        self.serializer = serializer

    def replace(self, text, current_version, new_version):
        _search_pattern = self.serializer.format(**current_version)
        _replace_pattern = self.serializer.format(**new_version)

        return text.replace(_search_pattern, _replace_pattern)
