import sys

class ConfigFile(object):
    def __init__(self, filepath):
        if sys.version_info < (3, 0):
            import imp

            self.configuration = imp.load_source("punch_config", filepath)

        elif sys.version_info < (3, 5):
            from importlib.machinery import SourceFileLoader

            try:
                self.configuration = SourceFileLoader("punch_config", filepath).load_module()
            except FileNotFoundError:
                raise ValueError("The configuration file {} cannot be found.".format(filepath))
            except ImportError:
                raise ValueError("The configuration file {} cannot imported due to an error.".format(filepath))
        else:
            import importlib.util

            spec = importlib.util.spec_from_file_location("punch_config", filepath)
            self.configuration = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(self.configuration)

        if self.configuration.__config_version__ > 1:
            raise ValueError("Unsupported configuration file version {}".format(self.configuration.__config_version__))