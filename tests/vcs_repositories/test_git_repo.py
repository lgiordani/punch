import os
import subprocess

import pytest

from punch.vcs_repositories import git_repo as gr, exceptions as re

pytestmark = pytest.mark.slow


@pytest.fixture
def temp_empty_git_dir(temp_empty_dir):
    subprocess.check_call(["git", "init", "-q", temp_empty_dir])
    subprocess.Popen(["git", "config", "user.email", "py.test@email.com"], cwd=temp_empty_dir)
    subprocess.Popen(["git", "config", "user.name", "PyTest"], cwd=temp_empty_dir)

    return temp_empty_dir


@pytest.fixture
def temp_git_dir(temp_empty_git_dir, safe_devnull):
    with open(os.path.join(temp_empty_git_dir, "README.md"), "w") as f:
        f.writelines(["# Test file", "This is just a test file for punch"])

    subprocess.Popen(["git", "add", "README.md"], cwd=temp_empty_git_dir, stdout=safe_devnull)
    subprocess.Popen(["git", "commit", "-m", "Initial addition"], cwd=temp_empty_git_dir,
                     stdout=safe_devnull)

    return temp_empty_git_dir


def test_get_current_branch(temp_git_dir):
    repo = gr.GitRepo(temp_git_dir)
    assert repo.get_current_branch() == 'master'


def test_get_tags(temp_git_dir):
    repo = gr.GitRepo(temp_git_dir)
    assert repo.get_tags() == ''


def test_init(temp_empty_git_dir):
    repo = gr.GitRepo(temp_empty_git_dir)

    assert repo.working_path == temp_empty_git_dir


def test_init_with_uninitialized_dir(temp_empty_dir):
    with pytest.raises(re.RepositorySystemError) as exc:
        gr.GitRepo(temp_empty_dir)

    assert str(exc.value) == "The current directory {} is not a Git repository".format(temp_empty_dir)


def test_pre_start_release(temp_git_dir):
    repo = gr.GitRepo(temp_git_dir)
    repo.pre_start_release()

    assert repo.get_current_branch() == 'master'


def test_pre_start_release_starting_from_different_branch(temp_git_dir, safe_devnull):
    subprocess.Popen(["git", "checkout", "-b", "new_branch"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)

    repo = gr.GitRepo(temp_git_dir)
    repo.pre_start_release()

    assert repo.get_current_branch() == 'master'


def test_pre_start_release_starting_from_different_branch_with_unstaged_changes(temp_git_dir, safe_devnull):
    subprocess.Popen(["git", "checkout", "-b", "new_branch"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)
    with open(os.path.join(temp_git_dir, "README.md"), "w") as f:
        f.writelines(["Unstaged lines"])

    repo = gr.GitRepo(temp_git_dir)
    repo.pre_start_release()

    assert repo.get_current_branch() == 'master'


def test_pre_start_release_starting_from_different_branch_with_uncommitted_changes(temp_git_dir, safe_devnull):
    subprocess.Popen(["git", "checkout", "-b", "new_branch"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)
    with open(os.path.join(temp_git_dir, "README.md"), "w") as f:
        f.writelines(["Unstaged lines"])
    subprocess.Popen(["git", "add", "README.md"], cwd=temp_git_dir, stdout=safe_devnull,
                     stderr=safe_devnull)

    repo = gr.GitRepo(temp_git_dir)
    with pytest.raises(re.RepositoryStatusError) as exc:
        repo.pre_start_release()


def test_start_release(temp_git_dir):
    repo = gr.GitRepo(temp_git_dir, {'new_version': 'a_release'})
    repo.pre_start_release()
    repo.start_release()
    assert repo.get_current_branch() == "a_release"


def test_finish_release_without_changes(temp_git_dir):
    release_name = "a_release"
    repo = gr.GitRepo(temp_git_dir, {'new_version': release_name})
    repo.pre_start_release()
    repo.start_release()
    repo.finish_release()
    assert repo.get_current_branch() == "master"
    assert release_name not in repo.get_branches()
    assert release_name not in repo.get_tags()


def test_finish_release_with_message(temp_git_dir):
    release_name = "1.0"
    commit_message = "A commit message"
    repo = gr.GitRepo(temp_git_dir, {'commit_message': commit_message, 'new_version': release_name})
    repo.pre_start_release()
    repo.start_release()

    with open(os.path.join(temp_git_dir, "version.txt"), "w") as f:
        f.writelines([release_name])

    repo.finish_release()

    p = subprocess.Popen(["git", "log"], cwd=temp_git_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    assert commit_message in stdout.decode('utf8')

    assert release_name in repo.get_tags()
    assert release_name not in repo.get_branches()


def test_finish_release_with_custom_tag(temp_git_dir):
    release_name = "1.0"
    commit_message = "A commit message"
    tag = "Version_{}".format(release_name)
    repo = gr.GitRepo(temp_git_dir, {'commit_message': commit_message, 'new_version': release_name, 'tag': tag})
    repo.pre_start_release()
    repo.start_release()

    with open(os.path.join(temp_git_dir, "version.txt"), "w") as f:
        f.writelines([release_name])

    repo.finish_release()

    assert tag in repo.get_tags()


def test_finish_release_custom_tag_cannot_contain_spaces(temp_git_dir):
    release_name = "1.0"
    commit_message = "A commit message"
    tag = "Version {}".format(release_name)

    with pytest.raises(re.RepositoryConfigurationError):
        gr.GitRepo(temp_git_dir, {'commit_message': commit_message, 'new_version': release_name, 'tag': tag})


def test_finish_release_with_annotated_tag(temp_git_dir):
    release_name = "1.0"
    commit_message = "A commit message"
    annotation_message = "An annotation message"
    repo = gr.GitRepo(temp_git_dir, {
        'commit_message': commit_message,
        'new_version': release_name,
        'annotate_tags': True,
        'annotation_message': annotation_message
    })
    repo.pre_start_release()
    repo.start_release()

    with open(os.path.join(temp_git_dir, "version.txt"), "w") as f:
        f.writelines([release_name])

    repo.finish_release()

    p = subprocess.Popen(["git", "log"], cwd=temp_git_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    assert commit_message in stdout.decode('utf8')

    p = subprocess.Popen(["git", "show", release_name], cwd=temp_git_dir, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    assert annotation_message in stdout.decode('utf8')

    assert release_name in repo.get_tags()
    assert release_name not in repo.get_branches()


def test_tag(temp_git_dir):
    repo = gr.GitRepo(temp_git_dir)

    repo.tag("just_a_tag")

    assert "just_a_tag" in repo.get_tags()
