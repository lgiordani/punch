import subprocess

import os
import pytest
from punch import vcs_configuration as vc
from punch.vcs_repositories import novcs_repo as nr, exceptions as re

pytestmark = pytest.mark.slow


def test_get_current_branch(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)
    assert repo.get_current_branch() == ''


def test_get_tags(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)
    assert repo.get_tags() == ''


def test_init(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)

    assert repo.working_path == temp_empty_dir


def test_pre_start_release(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)
    repo.pre_start_release()

    assert repo.get_current_branch() == ''


def test_start_release(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)
    repo.start_release()
    assert repo.get_current_branch() == ''


def test_finish_release_develop(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)
    repo.finish_release()

    assert repo.get_current_branch() == ''


def test_post_finish_release_develop(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)
    repo.post_finish_release()

    assert repo.get_current_branch() == ''


def test_tag(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)
    repo.tag("just_a_tag")

    assert repo.get_tags() == ''


def test_get_info(temp_empty_dir):
    repo = nr.NoVCSRepo(temp_empty_dir, None)

    assert repo.get_info() == []
