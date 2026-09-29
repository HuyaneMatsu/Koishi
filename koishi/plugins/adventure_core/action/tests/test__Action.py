import vampytest

from ...options import option_battle_create, option_loot_create

from ..action import Action, action_create
from ..action_types import ACTION_TYPE_GARDENING


def test__action_create():
    action_id = 9930
    action_type = ACTION_TYPE_GARDENING
    duration = 10000
    weight = 2
    battle = (
        option_battle_create(False, 1, 1, False, 1, 1, 120, None),
        option_battle_create(False, 1, 2, False, 0, 7, 126, None),
    )
    loot = (
        option_loot_create(False, 1, 1, False, 1, 1, 130, 22, 2, 20, 1),
        option_loot_create(False, 1, 2, False, 2, 4, 132, 22, 2, 20, 1),
    )
    
    action = action_create(
        action_id,
        action_type,
        duration,
        weight,
        battle,
        loot,
    )
    
    vampytest.assert_instance(action, Action)
    vampytest.assert_instance(action.duration, int)
    vampytest.assert_instance(action.battle, tuple, nullable = True)
    vampytest.assert_instance(action.loot, tuple, nullable = True)
    vampytest.assert_instance(action.id, int)
    vampytest.assert_instance(action.type, int)
    vampytest.assert_instance(action.weight, int)
    
    vampytest.assert_eq(action.id, action_id)
    vampytest.assert_eq(action.type, action_type)
    vampytest.assert_eq(action.duration, duration)
    vampytest.assert_eq(action.weight, weight)
    vampytest.assert_eq(action.battle, battle)
    vampytest.assert_eq(action.loot, loot)
