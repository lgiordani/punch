import mock
from punch.vcs_use_cases import vcs_start_release as vsruc


def test_run():
    repo = mock.Mock()
    use_case = vsruc.VCSStartReleaseUseCase(repo)

    result = use_case.execute()

    assert repo.pre_start_release.called_with()
    assert repo.start_release.called_with()
    assert result == repo.start_release()
