from unittest import mock
from punch.vcs_use_cases import release as rel


def test_pre_start_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.pre_start_release()

    assert repo.pre_start_release.called


def test_start_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.start_release()

    assert repo.start_release.called


def test_finish_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.finish_release()

    assert repo.finish_release.called


def test_post_finish_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.post_finish_release()

    assert repo.post_finish_release.called
