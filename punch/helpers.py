import sys

def import_file(config_filepath, version_filepath):
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

    return configuration_module, version_module