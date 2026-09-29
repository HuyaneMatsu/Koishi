from collections import OrderedDict

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import adventure_create
from ..queries import adventure_save


def _iter_options():
    adventure_entry_id_0 = 9999
    adventure_entry_id_1 = 9998
    user_id_0 = 202508100000
    user_id_1 = 202508100001
    
    adventure = adventure_create(
        user_id_0,
        0,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure.entry_id = adventure_entry_id_0
    
    # Existing.
    yield (
        adventure,
        0,
        OrderedDict((
            (adventure_entry_id_0, None),
            (adventure_entry_id_1, None),
        )),
        OrderedDict((
            ((user_id_0, 0, 0), None),
            ((user_id_1, 0, 0), None),
        )),
        (
            adventure_entry_id_0,
            set(),
            set(),
            [
                adventure_entry_id_1,
                adventure_entry_id_0,
            ],
            [
                ((user_id_0, 0, 0), None),
                ((user_id_1, 0, 0), None),
            ],
        ),
    )
    
    adventure = adventure_create(
        user_id_0,
        0,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    
    # New.
    yield (
        adventure,
        adventure_entry_id_1,
        OrderedDict(),
        OrderedDict((
            ((user_id_0, 0, 0), None),
            ((user_id_1, 0, 0), None),
        )),
        (
            adventure_entry_id_1,
            {
                adventure_entry_id_1
            },
            {
                user_id_0,
            },
            [
                adventure_entry_id_1,
            ],
            [
                ((user_id_1, 0, 0), None)
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__adventure_save(adventure, adventure_entry_id, adventure_cache, adventure_listing_cache):
    """
    Tests whether ``adventure_save`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    adventure : ``Adventure``
        The adventure to store.
    
    adventure_entry_id : `int`
        The adventure's entry's identifier in the database (used for new adventures).
    
    adventure_cache : ``OrderedDict<int, None | Adventure>``
        Adventure cache to use.
    
    adventure_listing_cache : ``OrderedDict<(int, int, int), None | list<Adventure>>``
        Adventure listing cache to use.
    
    Returns
    -------
    output : `(int, set<list>, set<int>, list<int>, list<(int, int, int)>)`
    """
    adventure_cache = adventure_cache.copy()
    adventure_listing_cache = adventure_listing_cache.copy()
    adventures = {}
    adventures_active = {}
    
    query_called = 0
    
    async def query_adventure_save(input_adventure):
        nonlocal adventure
        nonlocal query_called
        vampytest.assert_is(input_adventure, adventure)
        query_called += 1
    
    
    async def query_adventure_save_new(input_adventure):
        nonlocal adventure
        nonlocal adventure_entry_id
        nonlocal query_called
        vampytest.assert_is(input_adventure, adventure)
        query_called += 1
        return adventure_entry_id
    
    
    mocked = vampytest.mock_globals(
        adventure_save,
        ADVENTURES = adventures,
        ADVENTURES_ACTIVE = adventures_active,
        ADVENTURE_CACHE = adventure_cache,
        ADVENTURE_LISTING_CACHE = adventure_listing_cache,
        query_adventure_save = query_adventure_save,
        query_adventure_save_new = query_adventure_save_new,
        recursion = 3,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked(adventure))
    
    await skip_ready_cycle()
    
    vampytest.assert_true(task.is_done())
    vampytest.assert_eq(query_called, 1)
    
    output = task.get_result()
    
    vampytest.assert_instance(output, type(None))
    
    return (
        adventure.entry_id,
        {*adventures.keys()},
        {*adventures_active.keys()},
        [*adventure_cache.keys()],
        [*adventure_listing_cache.items()],
    )
