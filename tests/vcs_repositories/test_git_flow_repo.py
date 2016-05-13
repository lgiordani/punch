import os
import subprocess

import pytest

from punch.vcs_repositories import git_flow_repo as gfr, exceptions as re

pytestmark = pytest.mark.slow

@pytest.fixture
def temp_empty_git_dir(temp_empty_dir):
    subprocess.check_call(["git", "init", "-q", temp_empty_dir])
    subprocess.Popen(["git", "config", "user.email", "py.test@email.com"], cwd=temp_empty_dir)
    subprocess.Popen(["git", "config", "user.name", "PyTest"], cwd=temp_empty_dir)

    command_line = ["git", "flow", "init", "-d"]
    p = subprocess.Popen(command_line, cwd=temp_empty_dir, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)

    stdout, stderr = p.communicate()

    if p.returncode != 0:
        _error_text = "An error occurred executing '{}': {}\nProcess output was: {}"
        _error_message = _error_text.format(" ".join(command_line),
                                            stderr.decode('utf8'), stdout.decode('utf8'))

        raise ValueError(_error_message)

    return temp_empty_dir


@pytest.fixture
def temp_git_dir(temp_empty_git_dir, safe_devnull):
    with open(os.path.join(temp_empty_git_dir, "README.md"), "w") as f:
        f.writelines(["# Test file", "This is just a test file for punch"])

    subprocess.Popen(["git", "add", "README.md"], cwd=temp_empty_git_dir, stdout=safe_devnull)
    subprocess.Popen(["git", "commit", "-m", "Initial addition"], cwd=temp_empty_git_dir,
                     stdout=safe_devnull)

    return temp_empty_git_dir


def test_init(temp_empty_git_dir):
    repo = gfr.GitFlowRepo(temp_empty_git_dir)

    assert repo.working_path == temp_empty_git_dir


def test_get_current_branch(temp_git_dir):
    repo = gfr.GitFlowRepo(temp_git_dir)
    assert repo.get_current_branch() == 'develop'


def test_get_tags(temp_git_dir):
    repo = gfr.GitFlowRepo(temp_git_dir)
    assert repo.get_tags() == ''


def test_init_with_uninitialized_dir(temp_empty_dir):
    with pytest.raises(re.RepositorySystemError) as exc:
        gfr.GitFlowRepo(temp_empty_dir)

    assert str(exc.value) == "The current directory {} is not a Git repository".format(temp_empty_dir)


def test_pre_start_release(temp_git_dir):
    repo = gfr.GitFlowRepo(temp_git_dir)
    repo.pre_start_release()


def test_pre_start_release_starting_from_different_branch(temp_git_dir, safe_devnull):
    subprocess.Popen(["git", "checkout", "-b", "new_branch"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)

    repo = gfr.GitFlowRepo(temp_git_dir)
    repo.pre_start_release()

    assert repo.get_current_branch() == 'develop'


def test_pre_start_release_starting_from_different_branch_with_unstaged_changes(temp_git_dir, safe_devnull):
    subprocess.Popen(["git", "checkout", "-b", "new_branch"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)
    with open(os.path.join(temp_git_dir, "README.md"), "w") as f:
        f.writelines(["Unstaged lines"])

    repo = gfr.GitFlowRepo(temp_git_dir)

    repo.pre_start_release()

    assert repo.get_current_branch() == 'develop'


def test_pre_start_release_starting_from_different_branch_with_uncommitted_changes(temp_git_dir, safe_devnull):
    subprocess.Popen(["git", "checkout", "-b", "new_branch"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)
    with open(os.path.join(temp_git_dir, "README.md"), "w") as f:
        f.writelines(["Unstaged lines"])
    subprocess.Popen(["git", "add", "README.md"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)

    repo = gfr.GitFlowRepo(temp_git_dir)
    with pytest.raises(gfr.RepositoryStatusError):
        repo.pre_start_release()


def test_start_release(temp_git_dir):
    repo = gfr.GitFlowRepo(temp_git_dir)
    repo.pre_start_release()
    repo.start_release("a_release")
    assert repo.get_current_branch() == "release/a_release"


def test_finish_release_without_changes(temp_git_dir):
    release_name = "a_release"
    repo = gfr.GitFlowRepo(temp_git_dir)
    repo.pre_start_release()
    repo.start_release(release_name)
    repo.finish_release(release_name, "Commit_message")
    assert repo.get_current_branch() == "develop"
    assert release_name in repo.get_tags()


def test_finish_release_with_changes(temp_git_dir):
    release_name = "1.0"
    repo = gfr.GitFlowRepo(temp_git_dir)
    repo.pre_start_release()
    repo.start_release(release_name)

    with open(os.path.join(temp_git_dir, "version.txt"), "w") as f:
        f.writelines([release_name])

    repo.finish_release(release_name, "Commit_message")
    assert repo.get_current_branch() == "develop"
    assert release_name in repo.get_tags()

def test_post_finish_release(temp_git_dir):
    release_name = "1.0"
    repo = gfr.GitFlowRepo(temp_git_dir)
    repo.pre_start_release()
    repo.start_release(release_name)
    repo.finish_release(release_name, "Commit_message")
    repo.post_finish_release(release_name)

    assert repo.get_current_branch() == "develop"
    assert release_name in repo.get_tags()


