class RepositoryError(Exception):
    pass

class RepositoryWorkflowError(RepositoryError):
    pass

class RepositorySystemError(RepositoryError):
    pass


class RepositoryStatusError(RepositoryError):
    pass
