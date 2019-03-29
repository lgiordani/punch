import six

from punch.vcs_use_cases import tag

if six.PY2:
    import mock
else:
    from unittest import mock


def test_pre_tag():
    repo = mock.Mock()
    use_case = tag.VCSTagUseCase(repo)

    use_case.tag("just_a_tag")

    assert repo.tag.called_with("just_a_tag")
