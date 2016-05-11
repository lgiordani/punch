class VCSReleaseUseCase:
    def __init__(self, repo):
        self.repo = repo

    def pre_start_release(self, release=None):
        self.repo.pre_start_release(release)

    def start_release(self, release):
        self.repo.start_release(release)

    def finish_release(self, release, custom_message=None):
        self.repo.finish_release(release, custom_message)

    def post_finish_release(self, release):
        self.repo.post_finish_release(release)
