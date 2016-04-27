class VCSReleaseUseCase:
    def __init__(self, repo):
        self.repo = repo

    def pre_start_release(self):
        self.repo.pre_start_release()

    def start_release(self):
        self.repo.start_release()

    def finish_release(self):
        self.repo.finish_release()

    def post_finish_release(self):
        self.repo.post_finish_release()
