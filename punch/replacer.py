import mock


class Replacer:
    def __init__(self, config):
        self._config = config

    def replace(self, text, search_pattern, replace_pattern):
        _search_pattern = search_pattern.format(**self._config.GLOBALS)
        _replace_pattern = replace_pattern.format(**self._config.GLOBALS)

        return text.replace(_search_pattern, _replace_pattern)
