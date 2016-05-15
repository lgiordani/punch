# import mock
# import pytest
#
# from punch.vcs_repositories import exceptions as e
# from punch.vcs_use_cases import tag
#
#
# def test_pre_tag(temp_git_dir):
#     repo = mock.Mock()
#     use_case = tag.VCSTagUseCase(repo)
#
#     use_case.pre_tag("just_a_tag")
#
#     assert repo.pre_tag.called_with("just_a_tag")
