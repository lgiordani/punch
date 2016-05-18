from punch.vcs_use_cases import use_case


class VCSReleaseUseCase(use_case.VCSUseCase):
    def run(self, release, commit_message):
        self.pre_start_release(release)
        self.start_release(release)
        self.finish_release(release, commit_message)
        self.post_finish_release(release)
