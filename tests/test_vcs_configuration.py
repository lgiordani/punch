import pytest

from punch import vcs_configuration as vc


@pytest.fixture
def global_variables():
    return {
        'serializer': '{{ major }}.{{ minor }}.{{ patch }}',
        'mark': 'just a mark'
    }


@pytest.fixture
def vcs_configuration_dict():
    return {
        'name': 'git',
        'commit_message': "Version updated to {{ new_version }}",
        'finish_release': True,
        'options': {
            'make_release_branch': False,
            'annotate_tags': False,
            'annotation_message': '',
        }
    }


@pytest.fixture
def special_variables():
    return {
        'current_version': '1.2.3',
        'new_version': '1.3.0'
    }


def test_vcs_configuration_from_string(vcs_configuration_dict, global_variables, special_variables):
    vcsconf = vc.VCSConfiguration(vcs_configuration_dict['name'],
                                  vcs_configuration_dict['options'],
                                  global_variables,
                                  special_variables,
                                  vcs_configuration_dict['commit_message']
                                  )

    expected_options = {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': '',
        'current_version': '1.2.3',
        'new_version': '1.3.0'
    }

    assert vcsconf.name == 'git'
    assert vcsconf.commit_message == "Version updated to 1.3.0"
    assert vcsconf.finish_release is True
    assert vcsconf.options == expected_options


def test_vcs_configuration_from_dict(vcs_configuration_dict, global_variables, special_variables):
    vcsconf = vc.VCSConfiguration.from_dict(vcs_configuration_dict, global_variables, special_variables)

    expected_options = {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': '',
        'current_version': '1.2.3',
        'new_version': '1.3.0'
    }

    assert vcsconf.name == 'git'
    assert vcsconf.commit_message == "Version updated to 1.3.0"
    assert vcsconf.finish_release is True
    assert vcsconf.options == expected_options


def test_vcs_configuration_from_dict_without_commit_message(vcs_configuration_dict, global_variables,
                                                            special_variables):
    vcs_configuration_dict.pop('commit_message')
    vcsconf = vc.VCSConfiguration.from_dict(vcs_configuration_dict, global_variables, special_variables)

    expected_options = {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': '',
        'current_version': '1.2.3',
        'new_version': '1.3.0'
    }

    assert vcsconf.name == 'git'
    assert vcsconf.commit_message == "Version updated 1.2.3 -> 1.3.0"
    assert vcsconf.finish_release is True
    assert vcsconf.options == expected_options


def test_vcs_configuration_from_dict_without_finish_release(vcs_configuration_dict, global_variables,
                                                            special_variables):
    vcs_configuration_dict.pop('finish_release')
    vcsconf = vc.VCSConfiguration.from_dict(vcs_configuration_dict, global_variables, special_variables)

    expected_options = {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': '',
        'current_version': '1.2.3',
        'new_version': '1.3.0'
    }

    assert vcsconf.name == 'git'
    assert vcsconf.commit_message == "Version updated to 1.3.0"
    assert vcsconf.finish_release is True
    assert vcsconf.options == expected_options

def test_vcs_configuration_from_dict_without_options(vcs_configuration_dict, global_variables,
                                                                special_variables):
    vcs_configuration_dict.pop('options')
    vcsconf = vc.VCSConfiguration.from_dict(vcs_configuration_dict, global_variables, special_variables)

    assert vcsconf.name == 'git'
    assert vcsconf.commit_message == "Version updated to 1.3.0"
    assert vcsconf.finish_release is True


def test_vcs_configuration_from_dict_can_use_global_variables(vcs_configuration_dict, global_variables,
                                                              special_variables):
    vcs_configuration_dict['commit_message'] = "Mark: {{ mark }}"

    vcsconf = vc.VCSConfiguration.from_dict(vcs_configuration_dict, global_variables, special_variables)

    assert vcsconf.commit_message == "Mark: just a mark"


def test_vcs_configuration_from_dict_special_variables_take_precedence(vcs_configuration_dict, global_variables,
                                                                       special_variables):
    vcs_configuration_dict['commit_message'] = "{{ current_version }}"
    global_variables['current_version'] = "5.0.0"

    vcsconf = vc.VCSConfiguration.from_dict(vcs_configuration_dict, global_variables, special_variables)

    assert vcsconf.commit_message == "1.2.3"


def test_vcs_configuration_from_dict_options_templates_are_processed(vcs_configuration_dict, global_variables,
                                                                     special_variables):
    vcs_configuration_dict['options']['annotation_message'] = "Updated {{ current_version}} -> {{ new_version }}"
    vcsconf = vc.VCSConfiguration.from_dict(vcs_configuration_dict, global_variables, special_variables)

    expected_options = {
        'make_release_branch': False,
        'annotate_tags': False,
        'annotation_message': 'Updated 1.2.3 -> 1.3.0',
        'current_version': '1.2.3',
        'new_version': '1.3.0'
    }

    assert vcsconf.options == expected_options
