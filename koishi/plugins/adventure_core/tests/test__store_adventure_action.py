from collections import OrderedDict
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import AdventureAction
from ..queries import store_adventure_action


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
    
    # New entry
    yield (
        adventure_action_0,
        adventure_action_entry_id_0,
        OrderedDict(),
        [],
    )
    
    # Recently requested entry, empty
    yield (
        adventure_action_0,
        adventure_action_entry_id_0,
        OrderedDict((
            (adventure_entry_id, None),
        )),
        [
            (adventure_entry_id, [adventure_action_entry_id_0]),
        ],
    )
    
    # Recently requested entry, with one entry.
    yield (
        adventure_action_0,
        adventure_action_entry_id_0,
        OrderedDict((
            (adventure_entry_id, [adventure_action_1]),
        )),
        [
            (adventure_entry_id, [adventure_action_entry_id_1, adventure_action_entry_id_0]),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__store_adventure_action(adventure_action, adventure_action_entry_id, adventure_action_listing_cache):
    """
    Tests whether ``store_adventure_action`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure_action : ``AdventureAction``
        Adventure action to save.
    
    adventure_action_entry_id : `int`
        Adventure action entry identifier to use.
    
    adventure_action_listing_cache : ``OrderedDict<int, None | list<AdventureAction>>`
        Adventure actions cache to use.
    
    Returns
    -------
    output : `list<int, None | list<int>>`
    """
    adventure_action_listing_cache = type(adventure_action_listing_cache)([
        (key, (None if value is None else value.copy()))
        for key, value in adventure_action_listing_cache.items()
    ])
    
    async def query(input_adventure_action):
        nonlocal adventure_action_entry_id
        nonlocal adventure_action
        vampytest.assert_is(input_adventure_action, adventure_action)
        return adventure_action_entry_id
    
    mocked = vampytest.mock_globals(
        store_adventure_action,
        ADVENTURE_ACTION_LISTING_CACHE = adventure_action_listing_cache,
        query_store_adventure_action = query,
        recursion = 2,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked(adventure_action))
    
    await skip_ready_cycle()
    await skip_ready_cycle()
    await skip_ready_cycle()
    await skip_ready_cycle()
    vampytest.assert_true(task.is_done())
    
    vampytest.assert_eq(adventure_action.entry_id, adventure_action_entry_id)
    
    return [
        (key, (None if value is None else [element.entry_id for element in value]))
        for key, value in adventure_action_listing_cache.items()
    ]
