class VCSUseCase(object):
    def __init__(self, repo):
        self.repo = repo

    def __getattr__(self, item):
        return getattr(self.repo, item)
