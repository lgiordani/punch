import mock
from punch.vcs_use_cases import release as rel


def test_pre_start_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.pre_start_release()

    assert repo.pre_start_release.called
    assert repo.pre_start_release.called_with()


def test_pre_start_release_can_be_called_without_release_name():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.pre_start_release()

    assert repo.pre_start_release.called
    assert repo.pre_start_release.called_with()


def test_start_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.start_release()

    assert repo.start_release.called
    assert repo.start_release.called_with()


def test_finish_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.finish_release()

    assert repo.finish_release.called
    assert repo.finish_release.called_with()


def test_post_finish_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.post_finish_release()

    assert repo.post_finish_release.called
    assert repo.post_finish_release.called_with()
