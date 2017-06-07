import os

import re
import six

from punch.vcs_repositories import vcs_repo as vr
from punch.vcs_repositories import exceptions as e


class HgRepo(vr.VCSRepo):
    DEFAULT_BRANCH = 'default'

    def __init__(self, working_path, config_obj):
        if six.PY2:
            super(HgRepo, self).__init__(working_path, config_obj)
        else:
            super().__init__(working_path, config_obj)

        self.branch = self.config_obj.options.get('branch', 'default')
        self._recorded_branch = None

    def get_current_branch(self):
        stdout = self._run([self.command, "branch"])

        branch = stdout.replace("\n", "")

        return branch

    def get_branches(self):
        stdout = self._run([self.command, "branches"])
        return {self._parse_branch_line(l) for l in stdout.splitlines()}

    def get_tags(self):
        tags_str = self._run([self.command, "tags"])
        tags = map(
            lambda l: l.rsplit(" ", 1)[0].strip(),
            tags_str.splitlines()
        )
        return "\n".join(tags)

    def get_summary(self):
        output = self._run([self.command, "summary"])
        keys = {"branch", "commit", "update"}
        summary = {}
        for l in output.splitlines():
            try:
                k, body = l.split(": ", 1)
                if k in keys:
                    summary[k] = body
            except ValueError:
                pass

        return summary

    def pre_start_release(self):
        if not self._is_clean():
            raise e.RepositoryStatusError(
                "Cannot update default while repository" +
                " contains uncommitted changes")
        self._recorded_branch = self.get_current_branch()

        self._change_branch(self.branch)

        branch = self.get_current_branch()

        if branch != self.branch:
            raise e.RepositoryStatusError(
                "Current branch shall be {} but is {}".format(
                    self.branch, branch))

    def start_release(self):
        pass

    def finish_release(self):
        self.get_current_branch()
        try:
            if self._is_clean():
                return
            command_line = [self.command, "commit"]
            command_line.extend(["-m", self.config_obj.commit_message])
            self._run(command_line)
            tag = self._configured_tag()
            self.tag(tag)
        finally:
            self._recover_branch()

    def tag(self, tag):
        self._run([self.command, "tag", tag])

    def _recover_branch(self):
        if self._recorded_branch is not None:
            self._change_branch(self._recorded_branch)
            self._recorded_branch = None

    def _change_branch(self, branch):
        self._run([self.command, "update", branch])

    def _check_config(self):
        # Tag names cannot contain spaces
        tag = self.config_obj.options.get('tag', '')
        if ' ' in tag:
            raise e.RepositoryConfigurationError(
                """You specified "'tag': {}".""".format(tag) +
                " Tag names cannot contain spaces")
        if re.match("^\d+$", tag):
            raise e.RepositoryConfigurationError(
                """You specified "'tag': {}".""".format(tag) +
                " Tag names cannot be just digits")

    def _check_system(self):
        if six.PY2:
            super(HgRepo, self)._check_system()
        else:
            super()._check_system()

        if not os.path.exists(os.path.join(self.working_path, '.hg')):
            raise e.RepositorySystemError(
                "The current directory {} is not a Hg repository".format(
                    self.working_path))

    def _set_command(self):
        self.commands = ['hg']
        self.command = 'hg'

    def _is_clean(self):
        return self.get_summary()["commit"].endswith("(clean)")

    @classmethod
    def _parse_branch_line(cls, line):
        return re.match("(?P<tag>.+)\s+\d+:.+$", line).group("tag").strip()

    def _configured_tag(self):
        try:
            return self.config_obj.options['tag']
        except KeyError:
            return self.config_obj.options['new_version']
