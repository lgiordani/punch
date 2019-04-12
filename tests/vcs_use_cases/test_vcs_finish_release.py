import mock
from punch.vcs_use_cases import vcs_finish_release as vfruc


def test_run():
    repo = mock.Mock()
    use_case = vfruc.VCSFinishReleaseUseCase(repo)

    result = use_case.execute()

    assert repo.finish_release.called_with()
    assert repo.post_finish_release.called_with()
    assert result == repo.post_finish_release()
