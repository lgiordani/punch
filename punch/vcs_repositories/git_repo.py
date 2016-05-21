import os
import six
from punch.vcs_repositories import exceptions as e
from punch.vcs_repositories import vcs_repo as vr


class GitRepo(vr.VCSRepo):
    def __init__(self, working_path, config_obj):
        if six.PY2:
            super(GitRepo, self).__init__(working_path, config_obj)
        else:
            super().__init__(working_path, config_obj)

        self.make_release_branch = self.config_obj.options.get('make_release_branch', True)

    def _check_config(self):
        # Tag names cannot contain spaces
        tag = self.config_obj.options.get('tag', '')
        if ' ' in tag:
            raise e.RepositoryConfigurationError(
                """You specified "'tag': {}". Tag names cannot contain spaces""".format(tag))

    def _check_system(self):
        if six.PY2:
            super(GitRepo, self)._check_system()
        else:
            super()._check_system()

        if not os.path.exists(os.path.join(self.working_path, '.git')):
            raise e.RepositorySystemError("The current directory {} is not a Git repository".format(self.working_path))

    def _set_command(self):
        self.commands = ['git']
        self.command = 'git'

    def get_current_branch(self):
        stdout = self._run([self.command, "rev-parse", "--abbrev-ref", "HEAD"])

        branch = stdout.replace("\n", "")

        return branch

    def get_tags(self):
        return self._run([self.command, "tag"])

    def get_branches(self):
        return self._run([self.command, "branch"])

    def pre_start_release(self):
        output = self._run([self.command, "status"])
        if "Changes to be committed:" in output:
            raise e.RepositoryStatusError("Cannot checkout master while repository contains uncommitted changes")

        self._run([self.command, "checkout", "master"])

        branch = self.get_current_branch()

        if branch != "master":
            raise e.RepositoryStatusError("Current branch shall be master but is {}".format(branch))

    def start_release(self):
        if self.make_release_branch:
            self._run([self.command, "checkout", "-b", self.config_obj.options['new_version']])

    def finish_release(self):
        branch = self.get_current_branch()

        self._run([self.command, "add", "."])

        output = self._run([self.command, "status"])

        if "nothing to commit, working directory clean" in output and self.make_release_branch:
            self._run([self.command, "checkout", "master"])
            self._run([self.command, "branch", "-d", branch])
            return

        command_line = [self.command, "commit"]
        command_line.extend(["-m", self.config_obj.commit_message])

        self._run(command_line)

        if self.make_release_branch:
            self._run([self.command, "checkout", "master"])
            self._run([self.command, "merge", branch])
            self._run([self.command, "branch", "-d", branch])

        try:
            tag_value = self.config_obj.options['tag']
        except KeyError:
            tag_value = self.config_obj.options['new_version']

        if self.config_obj.options.get('annotate_tags', False):
            annotation_message = self.config_obj.options.get('annotation_message', "Version {{ new_version }}")
            self._run([self.command, "tag", "-a", tag_value, "-m", annotation_message])
        else:
            self._run([self.command, "tag", tag_value])

    def post_finish_release(self):
        pass

    def tag(self, tag_name):
        self._run([self.command, "tag", tag_name])
