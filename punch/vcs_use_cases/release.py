class VCSReleaseUseCase:
    def __init__(self, repo):
        self.repo = repo

    def pre_start_release(self, release=None):
        self.repo.pre_start_release(release)

    def start_release(self, release):
        self.repo.start_release(release)

    def finish_release(self, release, commit_message):
        self.repo.finish_release(release, commit_message)

    def post_finish_release(self, release):
        self.repo.post_finish_release(release)

    def run(self, release, commit_message):
        self.pre_start_release(release)
        self.start_release(release)
        self.finish_release(release, commit_message)
        self.post_finish_release(release)
