from collections import OrderedDict

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import Adventure
from ..queries import get_adventure


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
        adventure_entry_id,
        {},
        None,
        (
            0,
            set(),
            [
                adventure_entry_id,
            ],
        )
    )
    
    # Adventure already cached.
    yield (
        adventure_entry_id,
        OrderedDict((
            (adventure_entry_id, adventure),
        )),
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
        (
            adventure_entry_id,
            {adventure_entry_id},
            [adventure_entry_id],
        )
    )
    
    # New
    yield (
        adventure_entry_id,
        OrderedDict(),
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
        (
            adventure_entry_id,
            {adventure_entry_id},
            [adventure_entry_id],
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_adventure(adventure_entry_id, adventure_cache, results):
    """
    Tests whether ``get_adventure`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure_entry_id : `int`
        The adventure's entry's identifier in the database.
    
    adventure_cache : ``OrderedDict<int, Adventure>``
        Adventure cache to use.
    
    result : `None | list<dict<str, object>>`
        Entry to return by the query.
    
    Returns
    -------
    output : ``(int, set<int>, list<int>)``
    """
    adventure_cache = adventure_cache.copy()
    adventures = {}
    
    async def query(input_adventure_entry_id):
        nonlocal results
        nonlocal adventure_entry_id
        vampytest.assert_eq(input_adventure_entry_id, adventure_entry_id)
        return results
    
    mocked = vampytest.mock_globals(
        get_adventure,
        ADVENTURES = adventures,
        ADVENTURE_CACHE = adventure_cache,
        query_get_adventure = query,
        recursion = 2,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked(adventure_entry_id))
    
    await skip_ready_cycle()
    await skip_ready_cycle()
    await skip_ready_cycle()
    await skip_ready_cycle()
    
    vampytest.assert_true(task.is_done())
    
    output = task.get_result()
    
    vampytest.assert_instance(output, Adventure, nullable = True)
    
    return (
        (0 if output is None else output.entry_id),
        {*adventures.keys()},
        [*adventure_cache.keys()],
    )
