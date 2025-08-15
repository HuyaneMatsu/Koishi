import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..adventure import Adventure
from ..queries import get_active_adventure


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
    
    
    yield (
        user_id,
        {},
        None,
    )
    
    yield (
        user_id,
        {
            user_id : adventure,
        },
        adventure,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_active_adventure(user_id, adventures_active):
    """
    Tests whether ``get_active_adventure`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    adventures_active : ``dict<int, Adventure>``
        Adventure active cache to use.
    
    Returns
    -------
    output : ``None | Adventure``
    """
    adventures_active = adventures_active.copy()
    
    mocked = vampytest.mock_globals(
        get_active_adventure,
        ADVENTURES_ACTIVE = adventures_active,
    )
    
    loop = get_event_loop()
    task = Task(loop, mocked(user_id))
    
    await skip_ready_cycle()
    vampytest.assert_true(task.is_done())
    
    output = task.get_result()
    
    vampytest.assert_instance(output, Adventure, nullable = True)
    
    return output
