import pytest
import tempfile
import shutil

@pytest.fixture
def temp_empty_uninitialized_dir(request):
    tempdir = tempfile.mkdtemp()

    def fin():
        shutil.rmtree(tempdir)

    request.addfinalizer(fin)
    return tempdir
