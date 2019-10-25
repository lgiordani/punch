from __future__ import print_function, absolute_import, division

from collections import abc
from punch import file_configuration as fc
from punch.helpers import import_file


class ConfigurationVersionError(Exception):
    "An exception used to signal that the configuration file version is wrong"


class PunchConfig(object):

    def __init__(self, config_filepath):

        configuration_module = import_file(config_filepath)

        try:
            self.__config_version__ = configuration_module.__config_version__
        except AttributeError:
            raise ValueError(
                ("Given config file is invalid: "
                 "missing '__config_version__' variable")
            )

        if configuration_module.__config_version__ > 1:
            raise ConfigurationVersionError(
                ("Unsupported configuration file version "
                 "{}".format(configuration_module.__config_version__))
            )

        try:
            self.globals = configuration_module.GLOBALS
        except AttributeError:
            self.globals = {}

        try:
            files = configuration_module.FILES
        except AttributeError:
            raise ValueError(
                "Given config file is invalid: missing 'FILES' attribute")

        self.files = []
        for file_configuration in files:
            if isinstance(file_configuration, abc.Mapping):
                self.files.append(fc.FileConfiguration.from_dict(
                    file_configuration, self.globals))
            else:
                self.files.append(fc.FileConfiguration(
                    file_configuration, {}, self.globals))

        try:
            self.version = configuration_module.VERSION
        except AttributeError:
            raise ValueError(
                "Given config file is invalid: missing 'VERSION' attribute")

        try:
            self.vcs_serializer = configuration_module.VCS_SERIALIZER
        except AttributeError:
            self.vcs_serializer = '0'

        try:
            self.vcs = configuration_module.VCS
            if 'name' not in self.vcs.keys():
                raise ValueError("Missing key 'name' in VCS configuration")
        except AttributeError:
            self.vcs = None

        try:
            self.actions = configuration_module.ACTIONS
        except AttributeError:
            self.actions = {}

        self.actions.update(
            {
                'punch:increase': {
                    'type': 'increase_part'
                },
                'punch:set': {
                    'type': 'set_part'
                }
            }
        )

        try:
            self.release_notes = configuration_module.RELEASE_NOTES
        except AttributeError:
            self.release_notes = []
