from __future__ import print_function, absolute_import, division

from punch.vcs_use_cases import use_case


class VCSStartReleaseUseCase(use_case.VCSUseCase):
    def __init__(self, repo):
        self.repo = repo

    def execute(self):
        self.repo.pre_start_release()
        return self.repo.start_release()
