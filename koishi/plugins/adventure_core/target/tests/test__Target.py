import vampytest

from ..target import Target, target_create


def test__target_create():
    target_id = 9910
    name = 'Collect'
    duration_suggestion_set_id = 1233
    action_ids = (13315, 12323)
    
    target = target_create(
        target_id,
        name,
        duration_suggestion_set_id,
        action_ids,
    )
    
    vampytest.assert_instance(target, Target)
    vampytest.assert_instance(target.action_ids, tuple)
    vampytest.assert_instance(target.duration_suggestion_set_id, int)
    vampytest.assert_instance(target.id, int)
    vampytest.assert_instance(target.name, str)
    
    vampytest.assert_eq(target.id, target_id)
    vampytest.assert_eq(target.name, name)
    vampytest.assert_eq(target.duration_suggestion_set_id, duration_suggestion_set_id)
    vampytest.assert_eq(target.action_ids, action_ids)
