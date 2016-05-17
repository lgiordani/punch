import mock
from punch.vcs_use_cases import use_case


def test_delegate_all():
    repo = mock.Mock()
    uc = use_case.VCSUseCase(repo)

    uc.some_function("unnamed_parameter", named_parameter="named_parameter")

    assert repo.some_function.called_with("unnamed_parameter", named_parameter="named_parameter")


def test_delegate_override():
    repo = mock.Mock()

    class MyVCSUseCase(use_case.VCSUseCase):
        def some_function(self, *args, **kwds):
            pass

    uc = MyVCSUseCase(repo)
    uc.some_function("unnamed_parameter", named_parameter="named_parameter")

    assert not repo.some_function.called
