# -*- coding: utf-8 -*-

import re

from punch import version as ver
from punch import version_part as vp


class VersionParser:
    def __init__(self, config=None):
        if config is None:
            self.config = {}
        else:
            self.config = config

    def parse(self, version_string, regex):
        v = ver.Version()

        compiled_regex = re.compile(regex)
        match = compiled_regex.search(version_string)

        if match is None:
            raise ValueError

        for key, value in match.groupdict().items():
            try:
                part_config = self.config[key]
                part_type = part_config.pop('type')
            except KeyError:
                part_type = 'integer'
                part_config = {}

            class_name = part_type.title().replace("_", "") + 'VersionPart'
            cls = getattr(vp, class_name)

            v.add_part(key, value, cls, **part_config)

        return v