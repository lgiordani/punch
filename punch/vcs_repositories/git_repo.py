import os
import six

from punch.vcs_repositories import vcs_repo as vr
from punch.vcs_repositories import exceptions as e


class GitRepo(vr.VCSRepo):
    def __init__(self, working_path, config_obj=None):
        if six.PY2:
            super(GitRepo, self).__init__(working_path, config_obj)
        else:
            super().__init__(working_path, config_obj)

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

    def pre_start_release(self, release_name=None):
        output = self._run([self.command, "status"])
        if "Changes to be committed:" in output:
            raise e.RepositoryStatusError("Cannot checkout master while repository contains uncommitted changes")

        self._run([self.command, "checkout", "master"])

        branch = self.get_current_branch()

        if branch != "master":
            raise e.RepositoryStatusError("Current branch shall be master but is {}".format(branch))

    def start_release(self, release_name):
        self._run([self.command, "checkout", "-b", release_name])

    def finish_release(self, release_name, commit_message):
        branch = self.get_current_branch()

        self._run([self.command, "add", "."])

        output = self._run([self.command, "status"])

        if "nothing to commit, working directory clean" in output:
            self._run([self.command, "checkout", "master"])
            self._run([self.command, "branch", "-d", branch])
            return

        message = commit_message.format(release_name)

        command_line = [self.command, "commit"]
        command_line.extend(["-m", message])

        self._run(command_line)

        self._run([self.command, "checkout", "master"])
        self._run([self.command, "merge", branch])
        self._run([self.command, "branch", "-d", branch])
        self._run([self.command, "tag", release_name])

    def post_finish_release(self, release_name):
        pass

        # def pre_tag(self, tag_name):
        #     if not self.finish_release_called:
        #         raise e.RepositoryWorkflowError
        #     self._run([self.command, "tag", tag_name])
