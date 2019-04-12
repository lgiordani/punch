from __future__ import print_function, absolute_import, division

import os
import six
from punch.vcs_repositories import exceptions as e
from punch.vcs_repositories import vcs_repo as vr


class GitRepo(vr.VCSRepo):

    def __init__(self, working_path, config_obj, files_to_commit=None):
        if six.PY2:
            super(GitRepo, self).__init__(
                working_path, config_obj, files_to_commit)
        else:
            super().__init__(working_path, config_obj, files_to_commit)

        self.make_release_branch = self.config_obj.options.get(
            'make_release_branch',
            True
        )

        self.release_branch = self.config_obj.options['new_version']

        self.target_branch = self.config_obj.options.get(
            'target_branch',
            'master'
        )

        self.annotate_tags = self.config_obj.options.get(
            'annotate_tags',
            False
        )

        self.annotation_message = ''
        if self.annotate_tags:
            self.annotation_message = self.config_obj.options.get(
                'annotation_message',
                "Version {}".format(self.config_obj.options['new_version'])
            )

    def _check_config(self):
        # Tag names cannot contain spaces
        tag = self.config_obj.options.get('tag', '')
        if ' ' in tag:
            raise e.RepositoryConfigurationError(
                """You specified "'tag': {}".""".format(tag) +
                "Tag names cannot contain spaces")

    def _check_system(self):
        if six.PY2:
            super(GitRepo, self)._check_system()
        else:
            super()._check_system()

        if not os.path.exists(os.path.join(self.working_path, '.git')):
            raise e.RepositorySystemError(
                "The current directory {}".format(self.working_path) +
                " is not a Git repository")

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
            raise e.RepositoryStatusError(
                "Cannot checkout the target branch while repository" +
                " contains uncommitted changes"
            )

        self._run([self.command, "checkout", self.target_branch])

        branch = self.get_current_branch()

        if branch != self.target_branch:
            raise e.RepositoryStatusError(
                "Current branch should be {} (the target branch), " +
                "but is instead {}".format(
                    self.target_branch,
                    branch,
                )
            )

    def start_release(self):
        if self.make_release_branch:
            self._run([
                self.command,
                "checkout",
                "-b",
                self.release_branch
            ])

    def finish_release(self):
        branch = self.get_current_branch()

        command = [self.command, "add"]

        if self.config_obj.include_all_files:
            command.append(".")
        else:
            command.extend(self.config_obj.include_files)
            command.extend(self.files_to_commit)
        self._run(command)

        output = self._run([self.command, "status"])

        if ("nothing to commit, working directory clean" in output or
                "nothing to commit, working tree clean" in output) and \
                self.make_release_branch:
            self._run([self.command, "checkout", self.target_branch])
            self._run([self.command, "branch", "-d", branch])
            return

        command_line = [self.command, "commit"]
        command_line.extend(["-m", self.config_obj.commit_message])

        self._run(command_line)

        if self.make_release_branch:
            self._run([self.command, "checkout", self.target_branch])
            self._run([self.command, "merge", branch])
            self._run([self.command, "branch", "-d", branch])

        try:
            tag_value = self.config_obj.options['tag']
        except KeyError:
            tag_value = self.release_branch

        if self.config_obj.options.get('annotate_tags', False):
            annotation_message = self.config_obj.options.get(
                'annotation_message', "Version {{ new_version }}")
            self._run([
                self.command,
                "tag",
                "-a",
                tag_value,
                "-m",
                annotation_message
            ])
        else:
            self._run([self.command, "tag", tag_value])

    def post_finish_release(self):
        pass

    def tag(self, tag_name):
        self._run([self.command, "tag", tag_name])

    def get_info(self):
        return [
            ("Commit message", self.config_obj.commit_message),
            (
                "Create release branch",
                'yes' if self.make_release_branch else 'no'
            ),
            ("Release branch", self.release_branch),
            (
                "Annotate tags",
                'yes' if self.annotate_tags else 'no'
            ),
            ("Annotation message", self.annotation_message),
        ]
