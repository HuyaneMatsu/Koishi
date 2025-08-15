from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..adventure_action import AdventureAction


def _assert_fields_set(adventure_action):
    """
    Asserts whether the given adventure action has all of its fields set.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        The adventure action to check.
    """
    vampytest.assert_instance(adventure_action, AdventureAction)
    vampytest.assert_instance(adventure_action.action_id, int)
    vampytest.assert_instance(adventure_action.adventure_entry_id, int)
    vampytest.assert_instance(adventure_action.battle_data, bytes, nullable = True)
    vampytest.assert_instance(adventure_action.created_at, DateTime)
    vampytest.assert_instance(adventure_action.entry_id, int)
    vampytest.assert_instance(adventure_action.loot_data, bytes, nullable = True)
    vampytest.assert_instance(adventure_action.energy_exhausted, int)
    vampytest.assert_instance(adventure_action.health_exhausted, int)


def test__AdventureActivity__new():
    """
    Tests whether ``AdventureActivity.__new__`` works as intended.
    """
    adventure_entry_id = 12333
    action_id = 1233
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    battle_data = None
    loot_data = b'5' * 24
    health_exhausted = 0
    energy_exhausted = 63
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        action_id,
        created_at,
        battle_data,
        loot_data,
        health_exhausted,
        energy_exhausted,
    )
    
    _assert_fields_set(adventure_action)
    
    vampytest.assert_eq(adventure_action.action_id, action_id)
    vampytest.assert_eq(adventure_action.adventure_entry_id, adventure_entry_id)
    vampytest.assert_eq(adventure_action.battle_data, battle_data)
    vampytest.assert_eq(adventure_action.created_at, created_at)
    vampytest.assert_eq(adventure_action.loot_data, loot_data)
    vampytest.assert_eq(adventure_action.energy_exhausted, energy_exhausted)
    vampytest.assert_eq(adventure_action.health_exhausted, health_exhausted)


def test__AdventureActivity__repr():
    """
    Tests whether ``AdventureActivity.__new__`` works as intended.
    """
    adventure_entry_id = 12333
    action_id = 1233
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    battle_data = None
    loot_data = b'5' * 24
    health_exhausted = 0
    energy_exhausted = 63
    
    adventure_action = AdventureAction(
        adventure_entry_id,
        action_id,
        created_at,
        battle_data,
        loot_data,
        health_exhausted,
        energy_exhausted,
    )
    
    output = repr(adventure_action)
    vampytest.assert_instance(output, str)


def test__AdventureActivity__from_entry():
    """
    Tests whether ``AdventureActivity.__new__`` works as intended.
    """
    adventure_entry_id = 12333
    action_id = 1233
    created_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    battle_data = None
    loot_data = b'5' * 24
    health_exhausted = 0
    energy_exhausted = 63
    
    entry_id = 4566
    
    entry = {
        'adventure_entry_id' : adventure_entry_id,
        'action_id' : action_id,
        'created_at' : created_at.replace(tzinfo = None),
        'battle_data' : battle_data,
        'loot_data' : loot_data,
        'health_exhausted' : health_exhausted,
        'energy_exhausted' : energy_exhausted,
        
        'id' : entry_id
    }
    
    adventure_action = AdventureAction.from_entry(entry)
    
    _assert_fields_set(adventure_action)
    
    vampytest.assert_eq(adventure_action.action_id, action_id)
    vampytest.assert_eq(adventure_action.adventure_entry_id, adventure_entry_id)
    vampytest.assert_eq(adventure_action.battle_data, battle_data)
    vampytest.assert_eq(adventure_action.created_at, created_at)
    vampytest.assert_eq(adventure_action.loot_data, loot_data)
    vampytest.assert_eq(adventure_action.energy_exhausted, energy_exhausted)
    vampytest.assert_eq(adventure_action.health_exhausted, health_exhausted)
    
    vampytest.assert_eq(adventure_action.entry_id, entry_id)
