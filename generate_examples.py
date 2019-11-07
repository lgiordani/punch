#!/usr/bin/env python

import re

from jinja2 import Template

from punch.helpers import import_file


def process_multi_line(s):
    tmp = re.sub(r'^\n+', '', s)
    return re.sub(r'\n+$', '', tmp)


test_files = [
    'tests/script/test_action_conditional_reset_increment.py',
    'tests/script/test_action_conditional_reset_reset.py'
]

header = """
## Examples from the tests

The following examples are automatically extracted from the test suite.

"""

doc_page = """
### {{title}}

{{description}}

#### Version file
```
{{version_file}}
```

#### Configuration file
```
{{configuration_file}}
```

#### Effects
{% for name, content in test_files.items() %}
Original `{{name}}`
```
{{content['original']}}
```
Final `{{name}}`
```
{{content['expected']}}
```
{% endfor %}
"""

doc_page_template = Template(doc_page)

f = open('docs/test_examples.md', 'w')

f.write(header)

for test_file in test_files:
    test_module = import_file(test_file)

    try:
        test_module.test_name
    except AttributeError:
        # The file doesn't contain a test_name attribute
        # so it can't be used for the docs generation
        continue

    test_name = process_multi_line(test_module.test_name)
    test_description = process_multi_line(test_module.test_description)
    version_file_content = process_multi_line(test_module.version_file_content)
    config_file_content = process_multi_line(test_module.config_file_content)
    test_files = test_module.test_files

    render = doc_page_template.render(
        title=test_name,
        description=test_description,
        version_file=version_file_content,
        configuration_file=config_file_content,
        test_files=test_files,
    )

    f.write(render)
    print(render)

f.close()
