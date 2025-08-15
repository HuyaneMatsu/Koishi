from collections import OrderedDict

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import Adventure
from ..queries import store_adventure


def _iter_options():
    adventure_entry_id = 9999
    user_id_0 = 202508100000
    user_id_1 = 202508100001
    
    adventure = Adventure(
        user_id_0,
        0,
        0,
        0,
        0,
        0,
        0,
        0,
    )
    
    # No result.
    yield (
        adventure,
        adventure_entry_id,
        OrderedDict((
            ((user_id_0, 0, 0), None),
            ((user_id_1, 0, 0), None),
        )),
        (
            adventure_entry_id,
            {
                adventure_entry_id
            },
            {
                user_id_0,
            },
            [
                adventure_entry_id,
            ],
            [
                (user_id_1, 0, 0),
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__store_adventure(adventure, adventure_entry_id, adventure_listing_cache):
    """
    Tests whether ``store_adventure`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to store.
    
    adventure_entry_id : `int`
        The adventure's entry's identifier in the database.
    
    adventure_listing_cache : ``OrderedDict<(int, int, int), None | list<Adventure>>``
        Adventure listing cache to use.
    
    Returns
    -------
    output : ``(int, set<int>, set<list>, list<int>, list<(int, int, int)>)``
    """
    adventure_listing_cache = adventure_listing_cache.copy()
    adventure_cache = OrderedDict()
    adventures = {}
    adventures_active = {}
    
    async def query(input_adventure):
        nonlocal adventure
        nonlocal adventure_entry_id
        
        vampytest.assert_is(input_adventure, adventure)
        return adventure_entry_id
    
    mocked = vampytest.mock_globals(
        store_adventure,
        ADVENTURES = adventures,
        ADVENTURES_ACTIVE = adventures_active,
        ADVENTURE_CACHE = adventure_cache,
        ADVENTURE_LISTING_CACHE = adventure_listing_cache,
        query_store_adventure = query,
        recursion = 2,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked(adventure))
    
    await skip_ready_cycle()
    
    vampytest.assert_true(task.is_done())
    
    output = task.get_result()
    
    vampytest.assert_instance(output, type(None))
    
    return (
        adventure.entry_id,
        {*adventures.keys()},
        {*adventures_active.keys()},
        [*adventure_cache.keys()],
        [*adventure_listing_cache.keys()],
    )
