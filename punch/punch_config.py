import sys

import collections

from punch import version as ver
from punch import file_configuration as fc


class PunchConfig(object):
    def __init__(self, config_filepath, version_filepath):
        if sys.version_info < (3, 0):
            import imp

            configuration_module = imp.load_source("punch_config", config_filepath)
            version_module = imp.load_source("punch_version", version_filepath)

        elif sys.version_info < (3, 5):
            from importlib.machinery import SourceFileLoader

            try:
                configuration_module = SourceFileLoader("punch_config", config_filepath).load_module()
            except FileNotFoundError:
                raise ValueError("The configuration_module file {} cannot be found.".format(config_filepath))
            except ImportError:
                raise ValueError(
                    "The configuration_module file {} cannot imported due to an error.".format(config_filepath))

            try:
                version_module = SourceFileLoader("punch_version", version_filepath).load_module()
            except FileNotFoundError:
                raise ValueError("The version file {} cannot be found.".format(version_filepath))
            except ImportError:
                raise ValueError("The version file {} cannot imported due to an error.".format(version_filepath))

        else:
            import importlib.util

            spec = importlib.util.spec_from_file_location("punch_config", config_filepath)
            configuration_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(configuration_module)

            spec = importlib.util.spec_from_file_location("punch_version", version_filepath)
            version_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(version_module)

        try:
            self.__config_version__ = configuration_module.__config_version__
        except AttributeError:
            raise ValueError("Given config file is invalid: missing '__config_version__' variable")

        if configuration_module.__config_version__ > 1:
            raise ValueError(
                "Unsupported configuration file version {}".format(configuration_module.__config_version__))

        try:
            files = configuration_module.FILES
        except AttributeError:
            raise ValueError("Given config file is invalid: missing 'FILES' attribute")

        try:
            self.globals = configuration_module.GLOBALS
        except AttributeError:
            self.globals = {}

        self.files = []
        for file_configuration in files:
            if isinstance(file_configuration, collections.Mapping):
                self.files.append(fc.FileConfiguration.from_dict(file_configuration, self.globals))
            else:
                self.files.append(fc.FileConfiguration(file_configuration, {}, self.globals))

        try:
            version = configuration_module.VERSION
        except AttributeError:
            raise ValueError("Given config file is invalid: missing 'VERSION' attribute")

        self.version = ver.Version()

        for version_part in version:
            try:
                value = getattr(version_module, version_part['name'])
                version_part['value'] = value
            except AttributeError:
                raise ValueError("Given version file is invalid: missing '{}' variable".format(version_part['name']))

            self.version.add_part_from_dict(version_part)
