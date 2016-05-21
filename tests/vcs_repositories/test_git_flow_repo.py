import subprocess

import os
import pytest
from punch import vcs_configuration as vc
from punch.vcs_repositories import git_flow_repo as gfr, exceptions as re

pytestmark = pytest.mark.slow


@pytest.fixture
def temp_empty_git_dir(temp_empty_dir):
    subprocess.check_call(["git", "init", "-q", temp_empty_dir])
    subprocess.check_call(["git", "config", "user.email", "py.test@email.com"], cwd=temp_empty_dir)
    subprocess.check_call(["git", "config", "user.name", "PyTest"], cwd=temp_empty_dir)

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
def temp_gitflow_dir(temp_empty_git_dir, safe_devnull):
    with open(os.path.join(temp_empty_git_dir, "README.md"), "w") as f:
        f.writelines(["# Test file", "This is just a test file for punch"])

    subprocess.check_call(["git", "add", "README.md"], cwd=temp_empty_git_dir, stdout=safe_devnull)
    subprocess.check_call(["git", "commit", "-m", "Initial addition"], cwd=temp_empty_git_dir,
                     stdout=safe_devnull)

    return temp_empty_git_dir


@pytest.fixture
def empty_vcs_configuration():
    return vc.VCSConfiguration('git', {}, {}, {'current_version': 'a', 'new_version': 'b'})

def test_init(temp_empty_git_dir, empty_vcs_configuration):
    repo = gfr.GitFlowRepo(temp_empty_git_dir, empty_vcs_configuration)

    assert repo.working_path == temp_empty_git_dir


def test_get_current_branch(temp_gitflow_dir, empty_vcs_configuration):
    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    assert repo.get_current_branch() == 'develop'


def test_get_tags(temp_gitflow_dir, empty_vcs_configuration):
    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    assert repo.get_tags() == ''


def test_init_with_uninitialized_dir(temp_empty_dir, empty_vcs_configuration):
    with pytest.raises(re.RepositorySystemError) as exc:
        gfr.GitFlowRepo(temp_empty_dir, empty_vcs_configuration)

    assert str(exc.value) == "The current directory {} is not a Git repository".format(temp_empty_dir)


def test_pre_start_release(temp_gitflow_dir, empty_vcs_configuration):
    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    repo.pre_start_release()


def test_pre_start_release_starting_from_different_branch(temp_gitflow_dir, safe_devnull, empty_vcs_configuration):
    subprocess.check_call(["git", "checkout", "-b", "new_branch"], cwd=temp_gitflow_dir, stdout=safe_devnull,
                     stderr=safe_devnull)

    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    repo.pre_start_release()

    assert repo.get_current_branch() == 'develop'


def test_pre_start_release_starting_from_different_branch_with_unstaged_changes(temp_gitflow_dir, safe_devnull, empty_vcs_configuration):
    subprocess.check_call(["git", "checkout", "-b", "new_branch"], cwd=temp_gitflow_dir, stdout=safe_devnull,
                     stderr=safe_devnull)
    with open(os.path.join(temp_gitflow_dir, "README.md"), "w") as f:
        f.writelines(["Unstaged lines"])

    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)

    repo.pre_start_release()

    assert repo.get_current_branch() == 'develop'


def test_pre_start_release_starting_from_different_branch_with_uncommitted_changes(temp_gitflow_dir, safe_devnull, empty_vcs_configuration):
    subprocess.check_call(["git", "checkout", "-b", "new_branch"], cwd=temp_gitflow_dir, stdout=safe_devnull,
                     stderr=safe_devnull)
    with open(os.path.join(temp_gitflow_dir, "README.md"), "w") as f:
        f.writelines(["Unstaged lines"])
    subprocess.check_call(["git", "add", "README.md"], cwd=temp_gitflow_dir, stdout=safe_devnull,
                     stderr=safe_devnull)

    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    with pytest.raises(gfr.RepositoryStatusError):
        repo.pre_start_release()


def test_start_release(temp_gitflow_dir, empty_vcs_configuration):
    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    repo.pre_start_release()
    repo.start_release()
    assert repo.get_current_branch() == "release/b"


def test_finish_release_without_changes(temp_gitflow_dir, empty_vcs_configuration):
    release_name = empty_vcs_configuration.options['new_version']
    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    repo.pre_start_release()
    repo.start_release()
    repo.finish_release()
    assert repo.get_current_branch() == "develop"
    assert release_name not in repo.get_tags()


def test_finish_release_with_changes(temp_gitflow_dir, empty_vcs_configuration):
    release_name = empty_vcs_configuration.options['new_version']

    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)
    repo.pre_start_release()
    repo.start_release()

    with open(os.path.join(temp_gitflow_dir, "version.txt"), "w") as f:
        f.writelines([release_name])

    repo.finish_release()
    assert repo.get_current_branch() == "develop"
    assert release_name in repo.get_tags()


def test_tag(temp_gitflow_dir, empty_vcs_configuration):
    repo = gfr.GitFlowRepo(temp_gitflow_dir, empty_vcs_configuration)

    repo.tag("just_a_tag")

    assert "just_a_tag" in repo.get_tags()
