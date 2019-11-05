#!/usr/bin/env python

from punch.helpers import import_file

test_module = import_file(
    'tests/script/test_action_conditional_reset_increment.py')

with open('test.md', 'w'):
    print(test_module.test_description)
    print(test_module.version_file_content)
    print(test_module.config_file_content)
    print(test_module.test_files)
