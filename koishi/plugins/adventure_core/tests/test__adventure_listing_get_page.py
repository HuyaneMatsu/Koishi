from collections import OrderedDict

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import Adventure, adventure_create
from ..queries import adventure_listing_get_page


def _iter_options():
    user_id = 202508100003
    adventure_entry_id_0 = 9999
    adventure_entry_id_1 = 9998
    
    
    adventure_0 = adventure_create(
        user_id,
        0,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure_0.entry_id = adventure_entry_id_0
    
    adventure_1 = adventure_create(
        user_id,
        0,
        0,
        0,
        0,
        None,
        0,
        0,
        0,
    )
    adventure_1.entry_id = adventure_entry_id_1
    
    # No result.
    yield (
        user_id,
        10,
        10,
        OrderedDict(),
        1,
        [],
        (
            1,
            None,
            [
                ((user_id, 10, 10), (1, None)),
            ],
        ),
    )
    
    # requesting last page
    yield (
        user_id,
        -1,
        10,
        OrderedDict(),
        1,
        [],
        (
            1,
            None,
            [
                ((user_id, -1, 10), (1, None)),
                ((user_id, 0, 10), (1, None)),
            ],
        ),
    )
    
    # adventures already cached.
    yield (
        user_id,
        10,
        10,
        OrderedDict((
            ((user_id, 10, 10), (11, [adventure_0, adventure_1])),
        )),
        1,
            [
            {
                'id': adventure.entry_id,
                'user_id': adventure.user_id,
                
                'location_id': adventure.location_id,
                'target_id': adventure.target_id,
                'return_id': adventure.return_id,
                'auto_cancellation_id': adventure.auto_cancellation_id,
                'goal_listing_data': None,
                
                'initial_duration_seconds': adventure.initial_duration_seconds,
                'created_at': adventure.created_at,
                'updated_at': adventure.updated_at,
                'action_listing_data': None,
                'seed': adventure.seed,
                'state': adventure.state,
                
                'health_initial': adventure.health_initial,
                'health_exhausted': adventure.health_exhausted,
                
                'energy_initial': adventure.energy_initial,
                'energy_exhausted': adventure.energy_exhausted,
            }
            for adventure in (adventure_0, adventure_1)
        ],
        (
            11,
            [adventure_entry_id_0, adventure_entry_id_1],
            [
                ((user_id, 10, 10), (11, [adventure_entry_id_0, adventure_entry_id_1])),
            ],
        ),
    )
    
    # not cached.
    yield (
        user_id,
        10,
        10,
        OrderedDict(),
        11,
        [
            {
                'id': adventure.entry_id,
                'user_id': adventure.user_id,
                
                'location_id': adventure.location_id,
                'target_id': adventure.target_id,
                'return_id': adventure.return_id,
                'auto_cancellation_id': adventure.auto_cancellation_id,
                'goal_listing_data': None,
                
                'initial_duration_seconds': adventure.initial_duration_seconds,
                'created_at': adventure.created_at,
                'updated_at': adventure.updated_at,
                'action_listing_data': None,
                'seed': adventure.seed,
                'state': adventure.state,
                
                'health_initial': adventure.health_initial,
                'health_exhausted': adventure.health_exhausted,
                
                'energy_initial': adventure.energy_initial,
                'energy_exhausted': adventure.energy_exhausted,
            }
            for adventure in (adventure_0, adventure_1)
        ],
        (
            11,
            [adventure_entry_id_0, adventure_entry_id_1],
            [
                ((user_id, 10, 10), (11, [adventure_entry_id_0, adventure_entry_id_1])),
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__adventure_listing_get_page(
    user_id, page_index, page_size, adventure_listing_cache, page_count, results
):
    """
    Tests whether ``adventure_listing_get_page`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    page_index : `int`
        The page's index.
        If passed as negative, returns the last page.
    
    page_size : `int`
        The size of the page to get.
    
    adventure_listing_cache : ``OrderedDict<int, None | list<AdventureAction>>`
        Adventure actions cache to use.
    
    page_count : `int`
        Page count to return from query.
    
    results : `list<dict<str, object>>``
        Results to return from the query.
    
    Returns
    -------
    output : `(int, None | list<int>, list<(int, int, int), (int, None | list<int>)>)`
    """
    adventure_listing_cache = type(adventure_listing_cache)([
        (key, (value[0], (None if value[1] is None else value[1].copy())))
        for key, value in adventure_listing_cache.items()
    ])
    
    async def query(input_user_id, input_page_index, input_page_size):
        nonlocal page_count
        nonlocal results
        nonlocal user_id
        nonlocal page_index
        nonlocal page_size
        vampytest.assert_eq(input_user_id, user_id)
        vampytest.assert_eq(input_page_index, page_index)
        vampytest.assert_eq(input_page_size, page_size)
        return page_count, results
    
    mocked = vampytest.mock_globals(
        adventure_listing_get_page,
        ADVENTURE_LISTING_CACHE = adventure_listing_cache,
        query_adventure_listing_get_page = query,
        recursion = 2,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked(user_id, page_index, page_size))
    
    await skip_ready_cycle()
    await skip_ready_cycle()
    await skip_ready_cycle()
    await skip_ready_cycle()
    vampytest.assert_true(task.is_done())
    
    output = task.get_result()
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], int)
    vampytest.assert_instance(output[1], list, nullable = True)
    if (output[1] is not None):
        for element in output[1]:
            vampytest.assert_instance(element, Adventure)
    
    return (
        output[0],
        (None if output[1] is None else [element.entry_id for element in output[1]]),
        [
            (key, (value[0], (None if value[1] is None else [element.entry_id for element in value[1]])))
            for key, value in adventure_listing_cache.items()
        ],
    )
