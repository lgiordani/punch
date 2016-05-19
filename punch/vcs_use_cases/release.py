from punch.vcs_use_cases import use_case


class VCSReleaseUseCase(use_case.VCSUseCase):
    def run(self):
        self.pre_start_release()
        self.start_release()
        self.finish_release()
        self.post_finish_release()
