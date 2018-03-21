from __future__ import print_function, absolute_import, division


class RepositoryError(Exception):
    pass


class RepositoryWorkflowError(RepositoryError):
    pass


class RepositorySystemError(RepositoryError):
    pass


class RepositoryConfigurationError(RepositoryError):
    pass


class RepositoryStatusError(RepositoryError):
    pass
