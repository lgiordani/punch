import six

import pytest

import tempfile
import shutil
import os
import subprocess

@pytest.fixture
def temp_empty_uninitialized_dir(request):
    tempdir = tempfile.mkdtemp()

    def fin():
        shutil.rmtree(tempdir)

    request.addfinalizer(fin)
    return tempdir

@pytest.fixture
def safe_devnull():
    if six.PY2:
        devnull = open(os.devnull, 'w')

        def fin():
            devnull.close()

    else:
        devnull = subprocess.DEVNULL

    return devnull
