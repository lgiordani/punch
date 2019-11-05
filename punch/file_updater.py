from __future__ import print_function, absolute_import, division

import os
import six


class FileUpdater(object):

    def __init__(self, file_configuration, replacer):
        self.file_configuration = file_configuration
        self.replacer = replacer

    def get_summary(self, current_version, new_version):
        return self.replacer.run_all_serializers(current_version, new_version)

    def update(self, current_version, new_version):
        if not os.path.exists(self.file_configuration.path):
            if six.PY2:
                raise IOError(  # pragma: nocover
                    "The file {} does not exist".format(
                        self.file_configuration.path
                    )
                )
            else:
                raise FileNotFoundError(
                    "The file {} does not exist".format(
                        self.file_configuration.path
                    )
                )

        with open(self.file_configuration.path, 'r') as f:
            old_file_content = f.read()

        new_file_content = self.replacer.replace(
            old_file_content,
            current_version,
            new_version
        )

        if six.PY2:
            new_file_content = new_file_content.encode(
                'utf8')  # pragma: nocover

        if new_file_content == old_file_content:
            raise ValueError(
                "Cannot find any match for version {} in file {}".format(
                    current_version, self.file_configuration.path
                )
            )

        with open(self.file_configuration.path, 'w') as f:
            f.write(new_file_content)
