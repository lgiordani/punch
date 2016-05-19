import subprocess

import six
from punch.vcs_repositories.exceptions import RepositorySystemError


class VCSRepo(object):
    def __init__(self, working_path, config_obj):
        self.working_path = working_path
        self.config_obj = config_obj

        self._check_config()
        self._set_command()
        self._check_system()

    def _check_config(self):
        pass

    def _set_command(self):
        self.commands = [None]
        self.command = None

    def _check_system(self):
        null_commands = self.commands + ["--help"]

        if six.PY2:
            not_found_exception = IOError
        else:
            not_found_exception = FileNotFoundError

        try:
            if six.PY2:
                subprocess.check_output(null_commands)
            else:
                subprocess.check_call(null_commands, stdout=subprocess.DEVNULL)

        except not_found_exception:
            raise RepositorySystemError("Cannot run {}".format(self.command))
        except subprocess.CalledProcessError:
            raise RepositorySystemError("Error running {}".format(self.command))

    def _run(self, command_line, error_message=None):
        p = subprocess.Popen(command_line, cwd=self.working_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()

        if p.returncode != 0:
            if error_message is not None:
                raise RepositorySystemError(error_message.format(stderr))
            else:
                error_text = "An error occurred executing '{}': {}\nProcess output was: {}"
                error_message = error_text.format(" ".join(command_line),
                                                  stderr.decode('utf8'), stdout.decode('utf8'))
                raise RepositorySystemError(error_message)

        return stdout.decode('utf8')

    def pre_start_release(self):
        pass

    def start_release(self):
        pass

    def finish_release(self):
        pass

    def post_finish_release(self):
        pass
