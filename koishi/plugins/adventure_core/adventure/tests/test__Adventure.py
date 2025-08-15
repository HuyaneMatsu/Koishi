import vampytest
from scarletio import TimerHandle

from datetime import datetime as DateTime, timezone as TimeZone

from ..adventure import Adventure
from ..adventure_states import ADVENTURE_STATE_CANCELLED


def _assert_fields_set(adventure):
    """
    Asserts whether the given adventure has all of its fields set.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to check.
    """
    vampytest.assert_instance(adventure, Adventure)
    vampytest.assert_instance(adventure.action_count, int)
    vampytest.assert_instance(adventure.auto_cancellation_id, int)
    vampytest.assert_instance(adventure.created_at, DateTime)
    vampytest.assert_instance(adventure.energy_exhausted, int)
    vampytest.assert_instance(adventure.energy_initial, int)
    vampytest.assert_instance(adventure.entry_id, int)
    vampytest.assert_instance(adventure.handle, TimerHandle, nullable = True)
    vampytest.assert_instance(adventure.health_exhausted, int)
    vampytest.assert_instance(adventure.health_initial, int)
    vampytest.assert_instance(adventure.initial_duration, int)
    vampytest.assert_instance(adventure.location_id, int)
    vampytest.assert_instance(adventure.return_id, int)
    vampytest.assert_instance(adventure.seed, int)
    vampytest.assert_instance(adventure.state, int)
    vampytest.assert_instance(adventure.target_id, int)
    vampytest.assert_instance(adventure.updated_at, DateTime)
    vampytest.assert_instance(adventure.user_id, int)


def test__Adventure__new():
    """
    Tests whether ``Adventure.__new__`` works as intended.
    """
    user_id = 202507240000
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = Adventure(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        
        initial_duration,
        health_initial,
        energy_initial,
    )
    
    _assert_fields_set(adventure)
    
    vampytest.assert_eq(adventure.user_id, user_id)
    vampytest.assert_eq(adventure.location_id, location_id)
    vampytest.assert_eq(adventure.target_id, target_id)
    vampytest.assert_eq(adventure.return_id, return_id)
    vampytest.assert_eq(adventure.auto_cancellation_id, auto_cancellation_id)
    vampytest.assert_eq(adventure.initial_duration, initial_duration)
    vampytest.assert_eq(adventure.health_initial, health_initial)
    vampytest.assert_eq(adventure.energy_initial, energy_initial)


def test__Adventure__repr():
    """
    Tests whether ``Adventure.__repr__`` works as intended.
    """
    user_id = 202507240001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = Adventure(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        
        initial_duration,
        health_initial,
        energy_initial,
    )
    
    _assert_fields_set(adventure)
    
    vampytest.assert_eq(adventure.user_id, user_id)
    vampytest.assert_eq(adventure.location_id, location_id)
    vampytest.assert_eq(adventure.target_id, target_id)
    vampytest.assert_eq(adventure.return_id, return_id)
    vampytest.assert_eq(adventure.auto_cancellation_id, auto_cancellation_id)
    vampytest.assert_eq(adventure.initial_duration, initial_duration)
    vampytest.assert_eq(adventure.health_initial, health_initial)
    vampytest.assert_eq(adventure.energy_initial, energy_initial)


def test__Adventure__from_entry():
    """
    Tests whether ``Adventure.from_entry`` works as intended.
    """
    user_id = 202507240001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    entry_id = 123
    created_at = DateTime(2020, 5, 14, tzinfo = TimeZone.utc)
    updated_at = DateTime(2020, 5, 16, tzinfo = TimeZone.utc)
    action_count = 5
    seed = 15566556
    state = ADVENTURE_STATE_CANCELLED
    health_exhausted = 122
    energy_exhausted = 123
    
    
    entry = {
        'user_id': user_id,
        
        'location_id': location_id,
        'target_id': target_id,
        'return_id': return_id,
        'auto_cancellation_id': auto_cancellation_id,
        
        'initial_duration': initial_duration,
        'health_initial': health_initial,
        'energy_initial': energy_initial,
        
        'id': entry_id,
        'created_at': created_at.replace(tzinfo = None),
        'updated_at': updated_at.replace(tzinfo = None),
        'action_count': action_count,
        'seed': seed,
        'state': state,
        'health_exhausted': health_exhausted,
        'energy_exhausted': energy_exhausted,
    }
    
    adventure = Adventure.from_entry(entry)
    
    _assert_fields_set(adventure)
    
    vampytest.assert_eq(adventure.user_id, user_id)
    vampytest.assert_eq(adventure.location_id, location_id)
    vampytest.assert_eq(adventure.target_id, target_id)
    vampytest.assert_eq(adventure.return_id, return_id)
    vampytest.assert_eq(adventure.auto_cancellation_id, auto_cancellation_id)
    vampytest.assert_eq(adventure.initial_duration, initial_duration)
    vampytest.assert_eq(adventure.health_initial, health_initial)
    vampytest.assert_eq(adventure.energy_initial, energy_initial)
    
    vampytest.assert_eq(adventure.entry_id, entry_id)
    vampytest.assert_eq(adventure.created_at, created_at)
    vampytest.assert_eq(adventure.updated_at, updated_at)
    vampytest.assert_eq(adventure.action_count, action_count)
    vampytest.assert_eq(adventure.seed, seed)
    vampytest.assert_eq(adventure.state, state)
    vampytest.assert_eq(adventure.health_exhausted, health_exhausted)
    vampytest.assert_eq(adventure.energy_exhausted, energy_exhausted)
