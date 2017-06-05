import os
import subprocess
import textwrap
import tempfile
import shutil
import re

import pytest


class TestEnvironment(object):

    def __init__(self, path, script_runner):
        self.finalize = True
        self.path = path
        self.script_runner = script_runner

    def ensure_file_is_present(self, filename, content=""):
        with open(os.path.join(self.path, filename), "w") as f:
            f.write(textwrap.dedent(content))

    def get_file_content(self, filename):
        with open(os.path.join(self.path, filename), "r") as f:
            return f.read()

    def call(self, cmdline, **kwds):
        return self.script_runner.run(*cmdline, cwd=self.path, **kwds)

    def output(self, cmdline, **kwds):
        output = subprocess.check_output(cmdline, cwd=self.path, **kwds)
        return output.decode('utf8')

    def compare_output(self, expected_output, cmdline, **kwds):
        output = self.output(cmdline, **kwds)

        clean_expected_output = textwrap.dedent(expected_output)

        for line in clean_expected_output.split(os.linesep):
            reline = re.compile(line)
            l = reline.findall(output)
            assert len(l) > 0


@pytest.fixture
def test_environment(request, script_runner):
    tempdir = tempfile.mkdtemp()

    te = TestEnvironment(tempdir, script_runner)

    def fin():
        if te.finalize:
            shutil.rmtree(tempdir, ignore_errors=True)

    request.addfinalizer(fin)
    return te
