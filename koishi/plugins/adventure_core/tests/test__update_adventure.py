from collections import OrderedDict

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import Adventure
from ..queries import update_adventure


def _iter_options():
    adventure_entry_id_0 = 9999
    adventure_entry_id_1 = 9998
    user_id = 202508100002
    
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
    adventure.entry_id = adventure_entry_id_0
    
    # No result.
    yield (
        adventure,
        OrderedDict((
            (adventure_entry_id_0, None),
            (adventure_entry_id_1, None),
        )),
        [
            adventure_entry_id_1,
            adventure_entry_id_0,
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__update_adventure(adventure, adventure_cache):
    """
    Tests whether ``update_adventure`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to store.
    
    adventure_cache : ``OrderedDict<int, None | Adventure>``
        Adventure cache to use.
    
    Returns
    -------
    output : `list<int>`
    """
    adventure_cache = adventure_cache.copy()
    query_called = False
    
    async def query(input_adventure):
        nonlocal adventure
        nonlocal query_called
        vampytest.assert_is(input_adventure, adventure)
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        update_adventure,
        ADVENTURE_CACHE = adventure_cache,
        query_update_adventure = query,
        recursion = 2,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked(adventure))
    
    await skip_ready_cycle()
    
    vampytest.assert_true(task.is_done())
    vampytest.assert_eq(query_called, True)
    
    output = task.get_result()
    
    vampytest.assert_instance(output, type(None))
    
    return [*adventure_cache.keys()]
