import os
import six

from punch import replacer


class FileUpdater(object):
    def __init__(self, file_configuration):
        self.file_configuration = file_configuration
        self.rep = replacer.Replacer(file_configuration.config['serializer'])

    def get_summary(self, current_version, new_version):
        return self.rep.run_all_serializers(current_version, new_version)

    def update(self, current_version, new_version):
        if not os.path.exists(self.file_configuration.path):
            if six.PY2:
                raise IOError("The file {} does not exist".format(self.file_configuration.path))
            else:
                raise FileNotFoundError("The file {} does not exist".format(self.file_configuration.path))

        with open(self.file_configuration.path, 'r') as f:
            old_file_content = f.read()

        new_file_content = self.rep.replace(old_file_content, current_version, new_version)

        with open(self.file_configuration.path, 'w') as f:
            f.write(new_file_content)
