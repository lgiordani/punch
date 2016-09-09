import subprocess

import os
import pytest

import sys
from six.moves import configparser

from punch import vcs_configuration as vc
from punch.vcs_repositories import hg_repo as hr, exceptions as re
from tests.conftest import safe_devnull


pytestmark = pytest.mark.slow


def hg_repo_add_file(temp_hg_dir, fname, content="", out=None):
    if out is None:
        out = safe_devnull()

    with open(os.path.join(temp_hg_dir, fname), "w") as f:
        f.write(content)

    subprocess.check_call(["hg", "add", fname], cwd=temp_hg_dir, stdout=out)


def hg_repo_add_branch(temp_hg_dir, branch, message=None, out=None):
    if out is None:
        out = sys.stdout
    if message is None:
        message = "Starting new branch " + branch
    subprocess.check_call(["hg", "branch", "-f", branch], cwd=temp_hg_dir, stdout=out)
    subprocess.check_call(["hg", "commit", "-m", message], cwd=temp_hg_dir, stdout=out)


def hg_repo_change_branch(temp_hg_dir, branch, out=None):
    if out is None:
        out = sys.stdout
    subprocess.check_call(["hg", "update", branch], cwd=temp_hg_dir, stdout=out)


def hg_log(temp_hg_dir):
    p = subprocess.Popen(["hg", "log"], cwd=temp_hg_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    return stdout.decode('utf8')


@pytest.fixture
def temp_empty_hg_dir(temp_empty_dir):
    subprocess.check_call(["hg", "init", temp_empty_dir])

    hgrc = os.path.join(temp_empty_dir, ".hg", "hgrc")
    cp = configparser.ConfigParser()
    cp.read(hgrc)
    cp.add_section("ui")
    cp.set("ui", "username", "PyTest <py.test@email.com>")

    with open(hgrc, "w+") as f:
        cp.write(f)

    return temp_empty_dir


@pytest.fixture
def temp_hg_dir(temp_empty_hg_dir, safe_devnull):
    with open(os.path.join(temp_empty_hg_dir, "README.md"), "w") as f:
        f.writelines(["# Test file", "This is just a test file for punch"])

    subprocess.check_call(["hg", "add", "README.md"], cwd=temp_empty_hg_dir, stdout=safe_devnull)
    subprocess.check_call(["hg", "commit", "-m", "Initial addition"], cwd=temp_empty_hg_dir,
                          stdout=safe_devnull)

    return temp_empty_hg_dir


@pytest.fixture
def hg_other_branch(temp_hg_dir):
    hg_repo_add_branch(temp_hg_dir, "other")
    hg_repo_change_branch(temp_hg_dir, hr.HgRepo.DEFAULT_BRANCH)
    return temp_hg_dir


@pytest.fixture
def empty_vcs_configuration():
    return vc.VCSConfiguration('hg', {}, {}, {'current_version': 'a', 'new_version': 'b'})


@pytest.fixture
def other_branch_vcs_configuration():
    return vc.VCSConfiguration('hg', {"branch": "other"}, {}, {'current_version': 'a', 'new_version': 'b'})


@pytest.fixture
def ready_to_finish_repo(temp_hg_dir, **kwargs):
    release_name = "1.0"
    commit_message = "A commit message"
    config = vc.VCSConfiguration('git', kwargs, global_variables={}, special_variables={'new_version': release_name},
                                 commit_message=commit_message)

    repo = hr.HgRepo(temp_hg_dir, config)
    repo.pre_start_release()
    repo.start_release()

    hg_repo_add_file(temp_hg_dir, "version.txt", release_name + "\n")

    return repo


def test_init(temp_empty_hg_dir, empty_vcs_configuration):
    repo = hr.HgRepo(temp_empty_hg_dir, empty_vcs_configuration)
    assert repo.working_path == temp_empty_hg_dir


def test_init_with_uninitialized_dir(temp_empty_dir, empty_vcs_configuration):
    with pytest.raises(re.RepositorySystemError) as exc:
        hr.HgRepo(temp_empty_dir, empty_vcs_configuration)

    assert str(exc.value) == "The current directory {} is not a Hg repository".format(temp_empty_dir)


def test_get_current_branch(temp_hg_dir, empty_vcs_configuration):
    repo = hr.HgRepo(temp_hg_dir, empty_vcs_configuration)
    assert repo.get_current_branch() == repo.DEFAULT_BRANCH


def test_get_tags(temp_hg_dir, empty_vcs_configuration):
    repo = hr.HgRepo(temp_hg_dir, empty_vcs_configuration)
    assert repo.get_tags() == 'tip'


def test_pre_start_release(temp_hg_dir, empty_vcs_configuration):
    repo = hr.HgRepo(temp_hg_dir, empty_vcs_configuration)
    repo.pre_start_release()

    assert repo.get_current_branch() == repo.DEFAULT_BRANCH


def test_pre_start_release_start_from_different_branch(temp_hg_dir, empty_vcs_configuration):
    hg_dir = temp_hg_dir
    repo = hr.HgRepo(hg_dir, empty_vcs_configuration)
    hg_repo_add_branch(hg_dir, "other")
    repo.pre_start_release()
    assert repo.get_current_branch() == repo.DEFAULT_BRANCH


def test_pre_start_release_should_use_other_branch(temp_hg_dir, other_branch_vcs_configuration):
    hg_dir = temp_hg_dir
    repo = hr.HgRepo(hg_dir, other_branch_vcs_configuration)
    hg_repo_add_branch(hg_dir, "other")
    repo.pre_start_release()
    hg_repo_change_branch(hg_dir, repo.DEFAULT_BRANCH)
    repo.pre_start_release()
    assert repo.get_current_branch() == "other"


def test_pre_start_release_in_unclean_state(temp_hg_dir, empty_vcs_configuration):
    hg_dir = temp_hg_dir
    with open(os.path.join(hg_dir, "README.md"), "w") as f:
        f.writelines(["Uncommitted lines"])
    repo = hr.HgRepo(hg_dir, empty_vcs_configuration)
    with pytest.raises(re.RepositoryStatusError):
        repo.pre_start_release()

    assert repo.get_current_branch() == repo.DEFAULT_BRANCH


def test_pre_start_release_starting_from_different_branch_in_unclean_state(temp_hg_dir, empty_vcs_configuration):
    hg_dir = temp_hg_dir
    hg_repo_add_branch(hg_dir, "other")
    with open(os.path.join(hg_dir, "README.md"), "w") as f:
        f.writelines(["Uncommitted lines"])
    repo = hr.HgRepo(hg_dir, empty_vcs_configuration)
    with pytest.raises(re.RepositoryStatusError):
        repo.pre_start_release()

    assert repo.get_current_branch() == "other"


def test_start_release_should_be_in_defined_branch(hg_other_branch, other_branch_vcs_configuration):
    repo = hr.HgRepo(hg_other_branch, other_branch_vcs_configuration)
    repo.pre_start_release()
    repo.start_release()
    assert repo.get_current_branch() == "other"


def test_finish_release_without_changes(hg_other_branch, other_branch_vcs_configuration):
    repo = hr.HgRepo(hg_other_branch, other_branch_vcs_configuration)
    repo.pre_start_release()
    repo.start_release()
    repo.finish_release()
    assert repo.get_current_branch() == repo.DEFAULT_BRANCH
    assert 'b' not in repo.get_tags()


def test_finish_should_recover_start_branch(hg_other_branch, other_branch_vcs_configuration):
    hg_repo_add_branch(hg_other_branch, "third")
    repo = hr.HgRepo(hg_other_branch, other_branch_vcs_configuration)
    repo.pre_start_release()
    repo.start_release()
    repo.finish_release()
    assert repo.get_current_branch() == "third"


def test_finish_release_with_message(ready_to_finish_repo):
    d = ready_to_finish_repo.working_path
    config = ready_to_finish_repo.config_obj
    commit_message = config.commit_message

    ready_to_finish_repo.finish_release()

    log = hg_log(d)
    assert commit_message in log


def test_finish_release_without_release_branch(ready_to_finish_repo):
    config = ready_to_finish_repo.config_obj
    release_name = config.options['new_version']

    ready_to_finish_repo.finish_release()

    assert release_name not in ready_to_finish_repo.get_branches()


def test_finish_write_tag(ready_to_finish_repo):
    config = ready_to_finish_repo.config_obj
    release_name = config.options['new_version']

    ready_to_finish_repo.finish_release()

    assert release_name in ready_to_finish_repo.get_tags()


def test_finish_release_with_custom_tag(temp_hg_dir):
    tag = "Version_{}".format("1.0")
    repo = ready_to_finish_repo(temp_hg_dir, tag=tag)
    repo.finish_release()

    assert tag in repo.get_tags()


def test_finish_release_custom_tag_cannot_contain_spaces(temp_hg_dir):
    release_name = "1.0"
    commit_message = "A commit message"
    tag = "Version {}".format(release_name)

    config = vc.VCSConfiguration('hg', {'tag': tag}, global_variables={},
                                 special_variables={'new_version': release_name},
                                 commit_message=commit_message)

    with pytest.raises(re.RepositoryConfigurationError):
        hr.HgRepo(temp_hg_dir, config)


def test_finish_release_custom_tag_cannot_be_a_number(temp_hg_dir):
    release_name = "1.0"
    commit_message = "A commit message"
    tag = "12234"

    config = vc.VCSConfiguration('hg', {'tag': tag}, global_variables={},
                                 special_variables={'new_version': release_name},
                                 commit_message=commit_message)

    with pytest.raises(re.RepositoryConfigurationError):
        hr.HgRepo(temp_hg_dir, config)


def test_start_summary(temp_hg_dir, empty_vcs_configuration):
    repo = hr.HgRepo(temp_hg_dir, empty_vcs_configuration)
    repo.pre_start_release()
    assert repo.get_summary() == {"branch": "default", "commit": "(clean)",
                                  "update": "(current)"}


def test_get_branches(hg_other_branch, empty_vcs_configuration):
    repo = hr.HgRepo(hg_other_branch, empty_vcs_configuration)
    assert {"default", "other"} == repo.get_branches()


def test_tag(temp_hg_dir, empty_vcs_configuration):
    repo = hr.HgRepo(temp_hg_dir, empty_vcs_configuration)

    repo.tag("just_a_tag")

    assert "just_a_tag" in repo.get_tags()
