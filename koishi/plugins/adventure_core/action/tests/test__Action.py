import vampytest

from ...options import OptionBattle, OptionLoot

from ..action import Action
from ..action_types import ACTION_TYPE_GARDENING


def _assert_fields_set(action):
    """
    Asserts whether every fields are set of the given action.
    
    Parameters
    ----------
    action : ``Action``
    """
    vampytest.assert_instance(action, Action)
    vampytest.assert_instance(action.duration, int)
    vampytest.assert_instance(action.battle, tuple, nullable = True)
    vampytest.assert_instance(action.loot, tuple, nullable = True)
    vampytest.assert_instance(action.id, int)
    vampytest.assert_instance(action.type, int)
    vampytest.assert_instance(action.weight, int)


def test__Action__new():
    """
    Tests whether ``Action.__new__`` works as intended.
    """
    action_id = 9930
    action_type = ACTION_TYPE_GARDENING
    duration = 10000
    weight = 2
    battle = (
        OptionBattle(1, 1, 1, 1, 120, None),
        OptionBattle(1, 2, 0, 7, 126, None),
    )
    loot = (
        OptionLoot(1, 1, 1, 1, 130, 22, 2, 20, 1),
        OptionLoot(1, 2, 2, 4, 132, 22, 2, 20, 1),
    )
    
    action = Action(
        action_id,
        action_type,
        duration,
        weight,
        battle,
        loot,
    )
    
    _assert_fields_set(action)
    
    vampytest.assert_eq(action.id, action_id)
    vampytest.assert_eq(action.type, action_type)
    vampytest.assert_eq(action.duration, duration)
    vampytest.assert_eq(action.weight, weight)
    vampytest.assert_eq(action.battle, battle)
    vampytest.assert_eq(action.loot, loot)


def test__Action__repr():
    """
    Tests whether ``Action.__repr__`` works as intended.
    """
    action_id = 9930
    action_type = ACTION_TYPE_GARDENING
    duration = 10000
    weight = 2
    battle = (
        OptionBattle(1, 1, 1, 1, 120, None),
        OptionBattle(1, 2, 0, 7, 126, None),
    )
    loot = (
        OptionLoot(1, 1, 1, 1, 130, 22, 2, 20, 1),
        OptionLoot(1, 2, 2, 4, 132, 22, 2, 20, 1),
    )
    
    action = Action(
        action_id,
        action_type,
        duration,
        weight,
        battle,
        loot,
    )
    
    output = repr(action)
    vampytest.assert_instance(output, str)
