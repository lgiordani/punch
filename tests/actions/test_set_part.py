from punch import version
from punch.actions import set_part


def test_init():
    action_dict = {
        'minor': '4'
    }

    action = set_part.SetPartAction(action_dict)

    assert action.parts == action_dict


def test_process_version():
    v = version.Version()
    v.create_part('major', 4)
    v.create_part('minor', 3)
    v.create_part('patch', 1)

    action_dict = {
        'minor': '4'
    }

    action = set_part.SetPartAction(action_dict)

    new_version = action.process_version(v)

    assert new_version.get_part('major').value == 4
    assert new_version.get_part('minor').value == 4
    assert new_version.get_part('patch').value == 1
