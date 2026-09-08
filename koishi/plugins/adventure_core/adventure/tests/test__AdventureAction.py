import vampytest

from ..adventure_action import (
    AdventureAction, adventure_action_create, adventure_action_listing_deserialise, adventure_action_listing_serialise
)


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
    vampytest.assert_instance(adventure_action.battle_data, bytes, nullable = True)
    vampytest.assert_instance(adventure_action.created_at, int)
    vampytest.assert_instance(adventure_action.loot_data, bytes, nullable = True)
    vampytest.assert_instance(adventure_action.energy_exhausted, int)
    vampytest.assert_instance(adventure_action.health_exhausted, int)


def test__AdventureAction__repr():
    """
    Tests whether ``AdventureAction.__new__`` works as intended.
    """
    action_id = 1233
    created_at = 127000
    battle_data = None
    loot_data = b'5' * 24
    health_exhausted = 0
    energy_exhausted = 63
    
    adventure_action = adventure_action_create(
        action_id,
        created_at,
        battle_data,
        loot_data,
        health_exhausted,
        energy_exhausted,
    )
    
    output = repr(adventure_action)
    vampytest.assert_instance(output, str)


def test__adventure_action_create():
    """
    Tests whether ``adventure_action_create`` works as intended.
    """
    action_id = 1233
    created_at = 127000
    battle_data = None
    loot_data = b'5' * 24
    health_exhausted = 0
    energy_exhausted = 63
    
    adventure_action = adventure_action_create(
        action_id,
        created_at,
        battle_data,
        loot_data,
        health_exhausted,
        energy_exhausted,
    )
    
    _assert_fields_set(adventure_action)
    
    vampytest.assert_eq(adventure_action.action_id, action_id)
    vampytest.assert_eq(adventure_action.battle_data, battle_data)
    vampytest.assert_eq(adventure_action.created_at, created_at)
    vampytest.assert_eq(adventure_action.loot_data, loot_data)
    vampytest.assert_eq(adventure_action.energy_exhausted, energy_exhausted)
    vampytest.assert_eq(adventure_action.health_exhausted, health_exhausted)


def test__adventure_action_listing_serialise():
    """
    Tests whether ``adventure_action_listing_serialise`` works as intended.
    """
    adventure_action_0_action_id = 1233
    adventure_action_0_created_at = 127000
    adventure_action_0_battle_data = b'6' * 16
    adventure_action_0_loot_data = None
    adventure_action_0_health_exhausted = 2
    adventure_action_0_energy_exhausted = 63
    
    adventure_action_0 = adventure_action_create(
        adventure_action_0_action_id,
        adventure_action_0_created_at,
        adventure_action_0_battle_data,
        adventure_action_0_loot_data,
        adventure_action_0_health_exhausted,
        adventure_action_0_energy_exhausted,
    )
    
    adventure_action_1_action_id = 1234
    adventure_action_1_created_at = 127120
    adventure_action_1_battle_data = None
    adventure_action_1_loot_data = b'8' * 24
    adventure_action_1_health_exhausted = 0
    adventure_action_1_energy_exhausted = 12
    
    adventure_action_1 = adventure_action_create(
        adventure_action_1_action_id,
        adventure_action_1_created_at,
        adventure_action_1_battle_data,
        adventure_action_1_loot_data,
        adventure_action_1_health_exhausted,
        adventure_action_1_energy_exhausted,
    )
    
    output = adventure_action_listing_serialise([adventure_action_0, adventure_action_1])
    vampytest.assert_instance(output, bytes)
    vampytest.assert_eq(
        output,
        b''.join([
            adventure_action_0_action_id.to_bytes(4, 'little'),
            adventure_action_0_created_at.to_bytes(8, 'little'),
            len(adventure_action_0_battle_data).to_bytes(4, 'little'),
            (0).to_bytes(4, 'little'),
            adventure_action_0_health_exhausted.to_bytes(8, 'little'),
            adventure_action_0_energy_exhausted.to_bytes(8, 'little'),
            
            adventure_action_0_battle_data,
            
            adventure_action_1_action_id.to_bytes(4, 'little'),
            adventure_action_1_created_at.to_bytes(8, 'little'),
            (0).to_bytes(4, 'little'),
            len(adventure_action_1_loot_data).to_bytes(4, 'little'),
            adventure_action_1_health_exhausted.to_bytes(8, 'little'),
            adventure_action_1_energy_exhausted.to_bytes(8, 'little'),
            
            adventure_action_1_loot_data,
        ])
    )


def test__adventure_action_listing_deserialise():
    """
    Tests whether ``adventure_action_listing_deserialise`` works as intended.
    """
    adventure_action_0_action_id = 1233
    adventure_action_0_created_at = 127000
    adventure_action_0_battle_data = b'6' * 16
    adventure_action_0_loot_data = None
    adventure_action_0_health_exhausted = 2
    adventure_action_0_energy_exhausted = 63
    
    adventure_action_1_action_id = 1234
    adventure_action_1_created_at = 127120
    adventure_action_1_battle_data = None
    adventure_action_1_loot_data = b'8' * 24
    adventure_action_1_health_exhausted = 0
    adventure_action_1_energy_exhausted = 12
    
    data = b''.join([
        adventure_action_0_action_id.to_bytes(4, 'little'),
        adventure_action_0_created_at.to_bytes(8, 'little'),
        len(adventure_action_0_battle_data).to_bytes(4, 'little'),
        (0).to_bytes(4, 'little'),
        adventure_action_0_health_exhausted.to_bytes(8, 'little'),
        adventure_action_0_energy_exhausted.to_bytes(8, 'little'),
        
        adventure_action_0_battle_data,
        
        adventure_action_1_action_id.to_bytes(4, 'little'),
        adventure_action_1_created_at.to_bytes(8, 'little'),
        (0).to_bytes(4, 'little'),
        len(adventure_action_1_loot_data).to_bytes(4, 'little'),
        adventure_action_1_health_exhausted.to_bytes(8, 'little'),
        adventure_action_1_energy_exhausted.to_bytes(8, 'little'),
        
        adventure_action_1_loot_data,
    ])
    
    output = adventure_action_listing_deserialise(data)
    vampytest.assert_instance(output, list)
    vampytest.assert_eq(len(output), 2)
    for element in output:
        vampytest.assert_instance(element, AdventureAction)
    
    adventure_action_0, adventure_action_1 = output
    
    vampytest.assert_eq(adventure_action_0.action_id, adventure_action_0_action_id)
    vampytest.assert_eq(adventure_action_0.battle_data, adventure_action_0_battle_data)
    vampytest.assert_eq(adventure_action_0.created_at, adventure_action_0_created_at)
    vampytest.assert_eq(adventure_action_0.loot_data, adventure_action_0_loot_data)
    vampytest.assert_eq(adventure_action_0.energy_exhausted, adventure_action_0_energy_exhausted)
    vampytest.assert_eq(adventure_action_0.health_exhausted, adventure_action_0_health_exhausted)
    
    vampytest.assert_eq(adventure_action_1.action_id, adventure_action_1_action_id)
    vampytest.assert_eq(adventure_action_1.battle_data, adventure_action_1_battle_data)
    vampytest.assert_eq(adventure_action_1.created_at, adventure_action_1_created_at)
    vampytest.assert_eq(adventure_action_1.loot_data, adventure_action_1_loot_data)
    vampytest.assert_eq(adventure_action_1.energy_exhausted, adventure_action_1_energy_exhausted)
    vampytest.assert_eq(adventure_action_1.health_exhausted, adventure_action_1_health_exhausted)
