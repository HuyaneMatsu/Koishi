import vampytest
from scarletio import TimerHandle

from ....unit_core import AMOUNT_TYPE_COUNT

from ...goal import goal_create_default, goal_create_item_exact, goal_listing_serialise

from ..adventure import (
    ADVENTURE_MODIFICATION_FLAG_ACTION_LISTING, ADVENTURE_MODIFICATION_FLAG_ENERGY_EXHAUSTED,
    ADVENTURE_MODIFICATION_FLAG_HEALTH_EXHAUSTED, ADVENTURE_MODIFICATION_FLAG_STATE,
    ADVENTURE_MODIFICATION_FLAG_UPDATED_AT, Adventure, adventure_add_action, adventure_collect_modifications,
    adventure_count_actions_for_seeding, adventure_create, adventure_create_from_entry,
    adventure_increase_energy_exhausted, adventure_increase_health_exhausted, adventure_set_state,
    adventure_set_updated_at
)
from ..adventure_action import adventure_action_create, adventure_action_listing_serialise
from ..adventure_states import ADVENTURE_STATE_CANCELLED


def assert_adventure_fields_set(adventure):
    """
    Asserts whether the given adventure has all of its fields set.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to check.
    """
    vampytest.assert_instance(adventure, Adventure)
    vampytest.assert_instance(adventure.action_listing, list, nullable = True)
    vampytest.assert_instance(adventure.auto_cancellation_id, int)
    vampytest.assert_instance(adventure.created_at, int)
    vampytest.assert_instance(adventure.energy_exhausted, int)
    vampytest.assert_instance(adventure.energy_initial, int)
    vampytest.assert_instance(adventure.entry_id, int)
    vampytest.assert_instance(adventure.handle, TimerHandle, nullable = True)
    vampytest.assert_instance(adventure.health_exhausted, int)
    vampytest.assert_instance(adventure.health_initial, int)
    vampytest.assert_instance(adventure.goal_listing, list, nullable = True)
    vampytest.assert_instance(adventure.initial_duration_seconds, int)
    vampytest.assert_instance(adventure.location_id, int)
    vampytest.assert_instance(adventure.modification_flags, int)
    vampytest.assert_instance(adventure.return_id, int)
    vampytest.assert_instance(adventure.seed, int)
    vampytest.assert_instance(adventure.state, int)
    vampytest.assert_instance(adventure.target_id, int)
    vampytest.assert_instance(adventure.updated_at, int)
    vampytest.assert_instance(adventure.user_id, int)


def test__Adventure__repr():
    """
    Tests whether ``Adventure.__repr__`` works as intended.
    """
    user_id = 202507240001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    goal_listing = [
        goal_create_default(),
    ]
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        goal_listing,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    assert_adventure_fields_set(adventure)
    
    vampytest.assert_eq(adventure.user_id, user_id)
    vampytest.assert_eq(adventure.location_id, location_id)
    vampytest.assert_eq(adventure.target_id, target_id)
    vampytest.assert_eq(adventure.return_id, return_id)
    vampytest.assert_eq(adventure.auto_cancellation_id, auto_cancellation_id)
    vampytest.assert_eq(adventure.goal_listing, goal_listing)
    vampytest.assert_eq(adventure.initial_duration_seconds, initial_duration_seconds)
    vampytest.assert_eq(adventure.health_initial, health_initial)
    vampytest.assert_eq(adventure.energy_initial, energy_initial)


def test__adventure_create():
    """
    Tests whether ``adventure_create`` works as intended.
    """
    user_id = 202507240000
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    goal_listing = [
        goal_create_default(),
    ]
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        goal_listing,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    assert_adventure_fields_set(adventure)
    
    vampytest.assert_eq(adventure.user_id, user_id)
    vampytest.assert_eq(adventure.location_id, location_id)
    vampytest.assert_eq(adventure.target_id, target_id)
    vampytest.assert_eq(adventure.return_id, return_id)
    vampytest.assert_eq(adventure.auto_cancellation_id, auto_cancellation_id)
    vampytest.assert_eq(adventure.goal_listing, goal_listing)
    vampytest.assert_eq(adventure.initial_duration_seconds, initial_duration_seconds)
    vampytest.assert_eq(adventure.health_initial, health_initial)
    vampytest.assert_eq(adventure.energy_initial, energy_initial)



def test__adventure_create_from_entry():
    """
    Tests whether ``adventure_create_from_entry`` works as intended.
    """
    user_id = 202507240001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    goal_listing = [
        goal_create_item_exact(5, AMOUNT_TYPE_COUNT, 20),
    ]
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    entry_id = 123
    created_at = 1463184000
    updated_at = 1463356800
    action_listing = None
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
        'goal_listing_data': goal_listing_serialise(goal_listing),
        
        'initial_duration_seconds': initial_duration_seconds,
        'health_initial': health_initial,
        'energy_initial': energy_initial,
        
        'id': entry_id,
        'created_at': created_at,
        'updated_at': updated_at,
        'action_listing_data': None,
        'seed': seed,
        'state': state,
        'health_exhausted': health_exhausted,
        'energy_exhausted': energy_exhausted,
    }
    
    adventure = adventure_create_from_entry(entry)
    
    assert_adventure_fields_set(adventure)
    
    vampytest.assert_eq(adventure.user_id, user_id)
    vampytest.assert_eq(adventure.location_id, location_id)
    vampytest.assert_eq(adventure.target_id, target_id)
    vampytest.assert_eq(adventure.return_id, return_id)
    vampytest.assert_eq(adventure.auto_cancellation_id, auto_cancellation_id)
    vampytest.assert_eq(adventure.goal_listing, goal_listing)
    vampytest.assert_eq(adventure.initial_duration_seconds, initial_duration_seconds)
    vampytest.assert_eq(adventure.health_initial, health_initial)
    vampytest.assert_eq(adventure.energy_initial, energy_initial)
    
    vampytest.assert_eq(adventure.entry_id, entry_id)
    vampytest.assert_eq(adventure.created_at, created_at)
    vampytest.assert_eq(adventure.updated_at, updated_at)
    vampytest.assert_eq(adventure.action_listing, action_listing)
    vampytest.assert_eq(adventure.seed, seed)
    vampytest.assert_eq(adventure.state, state)
    vampytest.assert_eq(adventure.health_exhausted, health_exhausted)
    vampytest.assert_eq(adventure.energy_exhausted, energy_exhausted)


def test__adventure_set_state():
    """
    Tests whether ``adventure_set_state`` works as intended.
    """
    user_id = 202609010000
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        None,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    state_new = ADVENTURE_STATE_CANCELLED
    adventure_set_state(adventure, state_new)
    
    vampytest.assert_eq(adventure.state, state_new)
    vampytest.assert_true(adventure.modification_flags & ADVENTURE_MODIFICATION_FLAG_STATE)


def test__adventure_set_updated_at():
    """
    Tests whether ``adventure_set_updated_at`` works as intended.
    """
    user_id = 202609010001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        None,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    updated_at_new = 178100
    adventure_set_updated_at(adventure, updated_at_new)
    
    vampytest.assert_eq(adventure.updated_at, updated_at_new)
    vampytest.assert_true(adventure.modification_flags & ADVENTURE_MODIFICATION_FLAG_UPDATED_AT)


def test__adventure_add_action():
    """
    Tests whether ``adventure_add_action`` works as intended.
    """
    user_id = 202609010001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        None,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
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
    
    adventure_add_action(adventure, adventure_action)
    
    vampytest.assert_eq(adventure.action_listing, [adventure_action])
    vampytest.assert_true(adventure.modification_flags & ADVENTURE_MODIFICATION_FLAG_ACTION_LISTING)


def test__adventure_increase_energy_exhausted():
    """
    Tests whether ``adventure_increase_energy_exhausted`` works as intended.
    """
    user_id = 202609010001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        None,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    energy_exhausted_new = 23
    adventure_increase_energy_exhausted(adventure, energy_exhausted_new)
    
    vampytest.assert_eq(adventure.energy_exhausted, energy_exhausted_new)
    vampytest.assert_true(adventure.modification_flags & ADVENTURE_MODIFICATION_FLAG_ENERGY_EXHAUSTED)

    adventure_increase_energy_exhausted(adventure, energy_exhausted_new)
    
    vampytest.assert_eq(adventure.energy_exhausted, energy_exhausted_new << 1)


def test__adventure_increase_health_exhausted():
    """
    Tests whether ``adventure_increase_health_exhausted`` works as intended.
    """
    user_id = 202609010001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        None,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    health_exhausted_new = 23
    adventure_increase_health_exhausted(adventure, health_exhausted_new)
    
    vampytest.assert_eq(adventure.health_exhausted, health_exhausted_new)
    vampytest.assert_true(adventure.modification_flags & ADVENTURE_MODIFICATION_FLAG_HEALTH_EXHAUSTED)

    adventure_increase_health_exhausted(adventure, health_exhausted_new)
    
    vampytest.assert_eq(adventure.health_exhausted, health_exhausted_new << 1)


def test__adventure_collect_modifications():
    """
    Tests whether ``adventure_collect_modifications`` works as intended.
    """
    user_id = 202609010001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        None,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    adventure_action = adventure_action_create(
        123,
        127000,
        None,
        None,
        0,
        0,
    )
    health_exhausted_new = 23
    
    adventure_add_action(adventure, adventure_action)
    adventure_increase_health_exhausted(adventure, health_exhausted_new)
    
    output = adventure_collect_modifications(adventure)
    vampytest.assert_eq(
        output,
        {
            'action_listing_data': adventure_action_listing_serialise([adventure_action]),
            'health_exhausted': health_exhausted_new,
        },
    )
    vampytest.assert_eq(adventure.modification_flags, 0)


def test__adventure_count_actions_for_seeding():
    """
    Tests whether ``adventure_count_actions_for_seeding`` works as intended.
    """
    user_id = 202609010001
    location_id = 5666
    target_id = 4566
    return_id = 1222
    auto_cancellation_id = 5666
    initial_duration_seconds = 3600 * 8
    health_initial = 150
    energy_initial = 200
    
    
    adventure = adventure_create(
        user_id,
        
        location_id,
        target_id,
        return_id,
        auto_cancellation_id,
        None,
        
        initial_duration_seconds,
        health_initial,
        energy_initial,
    )
    
    vampytest.assert_eq(adventure_count_actions_for_seeding(adventure), 0)
    
    adventure_add_action(
        adventure,
        adventure_action_create(
            123,
            127000,
            None,
            None,
            0,
            0,
        ),
    )
    
    vampytest.assert_eq(adventure_count_actions_for_seeding(adventure), 1)
    
    adventure_add_action(
        adventure,
        adventure_action_create(
            23,
            127000,
            None,
            None,
            0,
            0,
        ),
    )
    
    vampytest.assert_eq(adventure_count_actions_for_seeding(adventure), 1)
