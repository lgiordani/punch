# -*- coding: utf-8 -*-

import re

from punch import version as ver


class VersionParser(object):
    def parse(self, version_string, regex):
        v = ver.Version()

        compiled_regex = re.compile(regex)
        match = compiled_regex.search(version_string)

        if match is None:
            raise ValueError

        for key, value in match.groupdict().items():
            v.add_part(key, value)

        return v