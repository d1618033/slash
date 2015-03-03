import os
import shutil
import tempfile

import pytest
from slash.frontend.slash_run import _iter_suite_file_paths


def test_iter_suite_paths_files_abspaths(filename, paths):
    with open(filename, 'w') as f:
        f.write('\n'.join(paths))

    assert list(_iter_suite_file_paths([filename])) == paths

def test_iter_suite_paths_files_relpath(filename, paths):
    with open(filename, 'w') as f:
        for path in paths:
            relpath = os.path.relpath(path, os.path.dirname(filename))
            assert not os.path.isabs(relpath)
            f.write(relpath)
            f.write('\n')

    assert list(_iter_suite_file_paths([filename])) == paths


@pytest.fixture
def filename(tmpdir):
    return str(tmpdir.join('filename.txt'))

@pytest.fixture
def paths(request, tmpdir):
    return [os.path.join(os.path.abspath(str(tmpdir)), 'file{0}.py'.format(i)) for i in range(10)]
