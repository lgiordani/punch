from __future__ import print_function, absolute_import, division

import sys


def import_file(filepath):
    if sys.version_info < (3, 0):
        import imp

        module = imp.load_source("punch_config", filepath)

    elif sys.version_info < (3, 5):
        from importlib.machinery import SourceFileLoader

        try:
            module = SourceFileLoader("punch_config", filepath).load_module()
        except FileNotFoundError:
            raise ValueError(
                "The module file {} cannot be found.".format(filepath))
        except ImportError:
            raise ValueError(
                "The module file {} cannot imported due to an error.".format(
                    filepath))

    else:
        import importlib.util

        spec = importlib.util.spec_from_file_location("punch_config", filepath)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

    return module


def optstr2dict(optstr, convert_boolean=False):
    def process_string(tup, convert_boolean=False):
        if not convert_boolean:
            return tup

        return (tup[0], tup[1].lower() == 'true')

    return dict(
        process_string(i.split('='), convert_boolean)
        for i in optstr.split(',')
    )
