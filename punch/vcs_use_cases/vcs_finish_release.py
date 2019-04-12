from __future__ import print_function, absolute_import, division

from punch.vcs_use_cases import use_case


class VCSFinishReleaseUseCase(use_case.VCSUseCase):
    def __init__(self, repo):
        self.repo = repo

    def execute(self):
        self.repo.finish_release()
        return self.repo.post_finish_release()
