class RepositoryError(Exception):
    pass

class RepositorySystemError(RepositoryError):
    pass


class RepositoryStatusError(RepositoryError):
    pass
