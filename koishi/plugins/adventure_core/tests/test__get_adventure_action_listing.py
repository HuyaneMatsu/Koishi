from collections import OrderedDict
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import AdventureAction
from ..queries import get_adventure_action_listing


def _iter_options():
    adventure_entry_id = 9999
    
    adventure_action_entry_id_0 = 8888
    adventure_action_entry_id_1 = 8889
    
    
    adventure_action_0 = AdventureAction(
        adventure_entry_id,
        999999,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        10,
    )
    adventure_action_0.entry_id = adventure_action_entry_id_0
    
    adventure_action_1 = AdventureAction(
        adventure_entry_id,
        999999,
        DateTime(2016, 5, 15, tzinfo = TimeZone.utc),
        None,
        None,
        0,
        10,
    )
    adventure_action_1.entry_id = adventure_action_entry_id_1
    
    # No result.
    yield (
        adventure_entry_id,
        OrderedDict(),
        [],
        (
            None,
            [
                (adventure_entry_id, None),
            ],
        ),
    )
    
    # adventure actions already cached.
    yield (
        adventure_entry_id,
        OrderedDict((
            (adventure_entry_id, [adventure_action_0, adventure_action_1]),
        )),
        [
            {
                'id': adventure_action.entry_id,
                'action_id': adventure_action.action_id,
                'adventure_entry_id': adventure_action.adventure_entry_id,
                'created_at': adventure_action.created_at.replace(tzinfo = None),
                
                'battle_data': adventure_action.battle_data,
                'loot_data': adventure_action.loot_data,
                
                'health_exhausted': adventure_action.health_exhausted,
                'energy_exhausted': adventure_action.energy_exhausted,
            }
            for adventure_action in (adventure_action_0, adventure_action_1)
        ],
        (
            [adventure_action_entry_id_0, adventure_action_entry_id_1],
            [
                (adventure_entry_id, [adventure_action_entry_id_0, adventure_action_entry_id_1]),
            ],
        ),
    )
    
    # not cached.
    yield (
        adventure_entry_id,
        OrderedDict(),
        [
            {
                'id': adventure_action.entry_id,
                'action_id': adventure_action.action_id,
                'adventure_entry_id': adventure_action.adventure_entry_id,
                'created_at': adventure_action.created_at.replace(tzinfo = None),
                
                'battle_data': adventure_action.battle_data,
                'loot_data': adventure_action.loot_data,
                
                'health_exhausted': adventure_action.health_exhausted,
                'energy_exhausted': adventure_action.energy_exhausted,
            }
            for adventure_action in (adventure_action_0, adventure_action_1)
        ],
        (
            [adventure_action_entry_id_0, adventure_action_entry_id_1],
            [
                (adventure_entry_id, [adventure_action_entry_id_0, adventure_action_entry_id_1]),
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_adventure_action_listing(adventure_entry_id, adventure_action_listing_cache, results):
    """
    Tests whether ``get_adventure_action_listing`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure_entry_id : `int`
        Adventure entry identifier to query actions of.
    
    adventure_action_listing_cache : ``OrderedDict<int, None | list<AdventureAction>>`
        Adventure actions cache to use.
    
    results : `list<dict<str, object>>``
        Results to return from the query.
    
    Returns
    -------
    output : `(None | list<int>, list<int, None | list<int>>)`
    """
    adventure_action_listing_cache = type(adventure_action_listing_cache)([
        (key, (None if value is None else value.copy()))
        for key, value in adventure_action_listing_cache.items()
    ])
    
    async def query(input_adventure_entry_id):
        nonlocal results
        nonlocal adventure_entry_id
        vampytest.assert_eq(input_adventure_entry_id, adventure_entry_id)
        return results
    
    mocked = vampytest.mock_globals(
        get_adventure_action_listing,
        ADVENTURE_ACTION_LISTING_CACHE = adventure_action_listing_cache,
        query_get_adventure_action_listing = query,
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
    
    vampytest.assert_instance(output, list, nullable = True)
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, AdventureAction)
    
    return (
        (None if output is None else [element.entry_id for element in output]),
        [
            (key, (None if value is None else [element.entry_id for element in value]))
            for key, value in adventure_action_listing_cache.items()
        ],
    )
