import sys

from punch import version as ver


class ConfigFile(object):
    def __init__(self, filepath):
        if sys.version_info < (3, 0):
            import imp

            configuration = imp.load_source("punch_config", filepath)

        elif sys.version_info < (3, 5):
            from importlib.machinery import SourceFileLoader

            try:
                configuration = SourceFileLoader("punch_config", filepath).load_module()
            except FileNotFoundError:
                raise ValueError("The configuration file {} cannot be found.".format(filepath))
            except ImportError:
                raise ValueError("The configuration file {} cannot imported due to an error.".format(filepath))
        else:
            import importlib.util

            spec = importlib.util.spec_from_file_location("punch_config", filepath)
            configuration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(configuration)

        try:
            self.__config_version__ = configuration.__config_version__
        except AttributeError:
            raise ValueError("Given config file is invalid: missing '__config_version__' attribute")

        if configuration.__config_version__ > 1:
            raise ValueError("Unsupported configuration file version {}".format(configuration.__config_version__))

        try:
            files = configuration.FILES
        except AttributeError:
            raise ValueError("Given config file is invalid: missing 'FILES' attribute")

        self.files = []
        for file_configuration in files:
            pass

        try:
            self.globals = configuration.GLOBALS
        except AttributeError:
            self.globals = {}

        try:
            version = configuration.VERSION
        except AttributeError:
            raise ValueError("Given config file is invalid: missing 'VERSION' attribute")

        self.version = ver.Version()

        for version_part in version:
            self.version.add_part_from_dict(version_part)
