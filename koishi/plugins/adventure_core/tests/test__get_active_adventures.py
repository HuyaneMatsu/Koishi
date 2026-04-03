from collections import OrderedDict

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import Adventure
from ..queries import get_active_adventures


def _iter_options():
    adventure_entry_id = 9999
    user_id = 202508090000
    
    adventure = Adventure(
        user_id,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    adventure.entry_id = adventure_entry_id
    
    # No result.
    yield (
        {},
        OrderedDict(),
        [],
        (
            [],
            set(),
            set(),
            [],
        )
    )
    
    # Adventure already cached.
    yield (
        {
            user_id : adventure,
        },
        OrderedDict((
            (adventure_entry_id, adventure),
        )),
        [
            {
                'id': adventure.entry_id,
                'user_id': adventure.user_id,
                
                'location_id': adventure.location_id,
                'target_id': adventure.target_id,
                'return_id': adventure.return_id,
                'auto_cancellation_id': adventure.auto_cancellation_id,
                'state': adventure.state,
                
                'initial_duration': adventure.initial_duration,
                'created_at': adventure.created_at.replace(tzinfo = None),
                'updated_at': adventure.updated_at.replace(tzinfo = None),
                'action_count': adventure.action_count,
                'seed': adventure.seed,
                
                'health_initial': adventure.health_initial,
                'health_exhausted': adventure.health_exhausted,
                
                'energy_initial': adventure.energy_initial,
                'energy_exhausted': adventure.energy_exhausted,
            },
        ],
        (
            [adventure_entry_id],
            {user_id},
            {adventure_entry_id},
            [adventure_entry_id],
        )
    )
    
    # New
    yield (
        {},
        OrderedDict(),
        [
            {
                'id': adventure.entry_id,
                'user_id': adventure.user_id,
                
                'location_id': adventure.location_id,
                'target_id': adventure.target_id,
                'return_id': adventure.return_id,
                'auto_cancellation_id': adventure.auto_cancellation_id,
                'state': adventure.state,
                
                'initial_duration': adventure.initial_duration,
                'created_at': adventure.created_at.replace(tzinfo = None),
                'updated_at': adventure.updated_at.replace(tzinfo = None),
                'action_count': adventure.action_count,
                'seed': adventure.seed,
                
                'health_initial': adventure.health_initial,
                'health_exhausted': adventure.health_exhausted,
                
                'energy_initial': adventure.energy_initial,
                'energy_exhausted': adventure.energy_exhausted,
            },
        ],
        (
            [adventure_entry_id],
            {user_id},
            {adventure_entry_id},
            [adventure_entry_id],
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_active_adventures(adventures_active, adventure_cache, results):
    """
    Tests whether ``get_active_adventures`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventures_active : ``dict<int, Adventure>``
        Adventure active cache to use.
    
    adventure_cache : ``OrderedDict<int, Adventure>``
        Adventure cache to use.
        
    results : `list<dict<str, object>>`
        List of entries to return by the query.
    
    Returns
    -------
    output : ``(list<int>, set<int>, set<int>, list<int>)``
    """
    adventures_active = adventures_active.copy()
    adventure_cache = adventure_cache.copy()
    adventures = {}
    
    async def query():
        nonlocal results
        return results
    
    mocked = vampytest.mock_globals(
        get_active_adventures,
        ADVENTURES_ACTIVE = adventures_active,
        ADVENTURES = adventures,
        ADVENTURE_CACHE = adventure_cache,
        query_get_active_adventures = query,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked())
    
    await skip_ready_cycle()
    vampytest.assert_true(task.is_done())
    
    output = task.get_result()
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Adventure)
    
    return (
        [element.entry_id for element in output],
        {*adventures_active.keys()},
        {*adventures.keys()},
        [*adventure_cache.keys()],
    )
