import vampytest

from ..target import Target


def _assert_fields_set(target):
    """
    Asserts whether every fields are set of the given target.
    
    Parameters
    ----------
    target : ``Target``
    """
    vampytest.assert_instance(target, Target)
    vampytest.assert_instance(target.action_ids, tuple)
    vampytest.assert_instance(target.duration_suggestion_set_id, int)
    vampytest.assert_instance(target.id, int)
    vampytest.assert_instance(target.name, str)


def test__Target__new():
    """
    Tests whether ``Target.__new__`` works as intended.
    """
    target_id = 9910
    name = 'Collect'
    duration_suggestion_set_id = 1233
    action_ids = (13315, 12323)
    
    target = Target(
        target_id,
        name,
        duration_suggestion_set_id,
        action_ids,
    )
    
    _assert_fields_set(target)
    
    vampytest.assert_eq(target.id, target_id)
    vampytest.assert_eq(target.name, name)
    vampytest.assert_eq(target.duration_suggestion_set_id, duration_suggestion_set_id)
    vampytest.assert_eq(target.action_ids, action_ids)


def test__Target__repr():
    """
    Tests whether ``Target.__new__`` works as intended.
    """
    target_id = 9910
    name = 'Collect'
    duration_suggestion_set_id = 1233
    action_ids = (13315, 12323)
    
    target = Target(
        target_id,
        name,
        duration_suggestion_set_id,
        action_ids,
    )
    
    output = repr(target)
    vampytest.assert_instance(output, str)
