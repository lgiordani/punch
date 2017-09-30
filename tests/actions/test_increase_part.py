from punch import version
from punch.actions import increase_part


def test_init():
    action_dict = {
        'part': 'somepart'
    }

    action = increase_part.IncreasePartAction(action_dict)

    assert action.part == 'somepart'


def test_process_version():
    v = version.Version()
    v.create_part('major', 4)
    v.create_part('minor', 3)
    v.create_part('patch', 1)

    action_dict = {
        'part': 'major'
    }

    action = increase_part.IncreasePartAction(action_dict)

    new_version = action.process_version(v)

    assert new_version.get_part('major').value == 5
    assert new_version.get_part('minor').value == 0
    assert new_version.get_part('patch').value == 0
