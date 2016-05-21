import six

import pytest

import tempfile
import shutil
import os
import subprocess


def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true",
                     help="run slow tests")


def pytest_runtest_setup(item):
    if 'slow' in item.keywords and not item.config.getvalue("runslow"):
        pytest.skip("need --runslow option to run")


@pytest.fixture
def temp_empty_dir(request):
    tempdir = tempfile.mkdtemp()

    # Make sure the directory is empty, there are some issues on Travis CI
    shutil.rmtree(tempdir, ignore_errors=True)
    os.mkdir(tempdir)

    def fin():
        shutil.rmtree(tempdir, ignore_errors=True)

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
