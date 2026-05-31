from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop

from ....bot_utils.models import DB_ENGINE

from ..queries import get_to_do_listing
from ..to_do import ToDo


@vampytest.skip_if(DB_ENGINE is not None)
async def test__get_to_do_listing__already_cached():
    """
    Tests whether ``get_to_do_listing`` works as intended.
    
    This function is a coroutine.
    
    Case: already cached.
    """
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605280000,
    )
    to_do.entry_id = 100
    
    mocked = vampytest.mock_globals(
        get_to_do_listing,
        2,
        TO_DO_LISTING = [to_do],
    )
    
    output = await mocked()
    vampytest.assert_eq(
        output,
        [to_do],
    )


@vampytest.skip_if(DB_ENGINE is not None)
async def test__get_to_do_listing__to_request():
    """
    Tests whether ``get_to_do_listing`` works as intended.
    
    This function is a coroutine.
    
    Case: to request.
    """
    mocked = vampytest.mock_globals(
        get_to_do_listing,
        2,
    )
    
    output = await mocked()
    vampytest.assert_eq(
        output,
        [],
    )


@vampytest.skip_if(DB_ENGINE is not None)
async def test__get_to_do_listing__to_request_parallel():
    """
    Tests whether ``get_to_do_listing`` works as intended.
    
    This function is a coroutine.
    
    Case: to request; parallel.
    """
    mocked = vampytest.mock_globals(
        get_to_do_listing,
        2,
    )
    
    loop = get_event_loop()
    task_0 = Task(loop, mocked())
    task_1 = Task(loop, mocked())
    
    output_0 = await task_0
    output_1 = await task_1
    
    vampytest.assert_is(output_0, output_1)
