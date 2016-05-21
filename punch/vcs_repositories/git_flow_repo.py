import subprocess

import os
import six
from punch.vcs_repositories import git_repo as gr
from punch.vcs_repositories.exceptions import RepositoryStatusError, RepositorySystemError


class GitFlowRepo(gr.GitRepo):
    def __init__(self, working_path, config_obj):
        if six.PY2:
            super(GitFlowRepo, self).__init__(working_path, config_obj)
        else:
            super().__init__(working_path, config_obj)

    def _set_command(self):
        self.commands = ['git', 'flow']
        self.command = 'git'

    def _check_system(self):
        # git flow -h returns 1 so the call fails

        p = subprocess.Popen(self.commands, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = p.communicate()

        if "git flow <subcommand>" not in stdout.decode('utf8'):
            raise RepositorySystemError("Cannot run {}".format(self.commands))

        if not os.path.exists(os.path.join(self.working_path, '.git')):
            raise RepositorySystemError("The current directory {} is not a Git repository".format(self.working_path))

    def pre_start_release(self):
        output = self._run([self.command, "status"])
        if "Changes to be committed:" in output:
            raise RepositoryStatusError("Cannot checkout master while repository contains uncommitted changes")

        self._run([self.command, "checkout", "develop"])

        branch = self.get_current_branch()

        if branch != "develop":
            raise RepositoryStatusError("Current branch shall be master but is {}".format(branch))

    def start_release(self):
        self._run(self.commands + ["release", "start", self.config_obj.options['new_version']])

    def finish_release(self):
        branch = self.get_current_branch()

        self._run([self.command, "add", "."])

        output = self._run([self.command, "status"])
        if "nothing to commit, working directory clean" in output:
            self._run([self.command, "checkout", "develop"])
            self._run([self.command, "branch", "-d", branch])
            return

        message = ["-m", self.config_obj.commit_message]

        command_line = [self.command, "commit"]
        command_line.extend(message)

        self._run(command_line)

        self._run(self.commands + ["release", "finish", "-m", branch, self.config_obj.options['new_version']])

    def post_finish_release(self):
        pass
