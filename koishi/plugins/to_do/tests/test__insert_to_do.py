from datetime import datetime as DateTime, timezone as TimeZone
from itertools import count

import vampytest

from ....bot_utils.models import DB_ENGINE

from ..queries import insert_to_do
from ..to_do import ToDo


@vampytest.skip_if(DB_ENGINE is not None)
async def test__insert_to_do__existing():
    """
    Tests whether ``insert_to_do`` works as intended.
    
    This function is a coroutine.
    
    Case: existing entry.
    """
    TO_DO_LISTING = []
    COUNTER = iter(count(1))
    
    entry_id = 100
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605280001,
    )
    to_do.entry_id = entry_id
    
    mocked = vampytest.mock_globals(
        insert_to_do,
        2,
        COUNTER = COUNTER,
        TO_DO_LISTING = TO_DO_LISTING,
    )
    
    await mocked(to_do)
    
    vampytest.assert_eq(TO_DO_LISTING, [])
    vampytest.assert_eq(to_do.entry_id, entry_id)


@vampytest.skip_if(DB_ENGINE is not None)
async def test__insert_to_do__new():
    """
    Tests whether ``insert_to_do`` works as intended.
    
    This function is a coroutine.
    
    Case: new entry.
    """
    TO_DO_LISTING = []
    COUNTER = iter(count(1))
    
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605280002,
    )
    
    mocked = vampytest.mock_globals(
        insert_to_do,
        2,
        COUNTER = COUNTER,
        TO_DO_LISTING = TO_DO_LISTING,
    )
    
    await mocked(to_do)
    
    vampytest.assert_eq(TO_DO_LISTING, [to_do])
    vampytest.assert_eq(to_do.entry_id, 1)
