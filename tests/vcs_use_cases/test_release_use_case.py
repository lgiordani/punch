import mock
from punch.vcs_use_cases import release as rel


def test_pre_start_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.pre_start_release("release_name")

    assert repo.pre_start_release.called
    assert repo.pre_start_release.called_with("release_name")


def test_pre_start_release_can_be_called_without_release_name():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.pre_start_release()

    assert repo.pre_start_release.called
    assert repo.pre_start_release.called_with()


def test_start_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.start_release("release_name")

    assert repo.start_release.called
    assert repo.start_release.called_with("release_name")


def test_finish_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.finish_release("release_name", "custom_message")

    assert repo.finish_release.called
    assert repo.finish_release.called_with("release_name", "custom_message")


def test_post_finish_release():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.post_finish_release("release_name")

    assert repo.post_finish_release.called
    assert repo.post_finish_release.called_with("release_name")


def test_run():
    repo = mock.Mock()
    use_case = rel.VCSReleaseUseCase(repo)

    use_case.run("release_name", "custom_message")
    assert repo.pre_start_release.called_with("release_name")
    assert repo.start_release.called_with("release_name")
    assert repo.finish_release.called_with("release_name", "custom_message")
    assert repo.post_finish_release.called_with("release_name")
