from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bot_utils.models import DB_ENGINE

from ..queries import delete_to_do
from ..to_do import ToDo


@vampytest.skip_if(DB_ENGINE is not None)
async def test__delete_to_do__existing():
    """
    Tests whether ``delete_to_do`` works as intended.
    
    This function is a coroutine.
    
    Case: existing entry.
    """
    TO_DO_LISTING = []
    query_delete_to_do_called = False
    
    entry_id = 100
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605280005,
    )
    to_do.entry_id = entry_id
    TO_DO_LISTING.append(to_do)
    
    
    async def query_delete_to_do_patched(input_to_do):
        nonlocal query_delete_to_do_called
        nonlocal to_do
        query_delete_to_do_called = True
        vampytest.assert_eq(input_to_do, to_do)
        
    
    mocked = vampytest.mock_globals(
        delete_to_do,
        2,
        TO_DO_LISTING = TO_DO_LISTING,
        query_delete_to_do = query_delete_to_do_patched,
    )
    
    await mocked(to_do)
    
    vampytest.assert_eq(TO_DO_LISTING, [])
    vampytest.assert_true(query_delete_to_do_called)


@vampytest.skip_if(DB_ENGINE is not None)
async def test__delete_to_do__new():
    """
    Tests whether ``delete_to_do`` works as intended.
    
    This function is a coroutine.
    
    Case: new entry.
    """
    TO_DO_LISTING = []
    query_delete_to_do_called = False
    
    
    to_do = ToDo(
        'shrimp',
        None,
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
        202605280006,
    )
    
    
    async def query_delete_to_do_patched(input_to_do):
        nonlocal query_delete_to_do_called
        nonlocal to_do
        query_delete_to_do_called = True
        vampytest.assert_eq(input_to_do, to_do)
    
    
    mocked = vampytest.mock_globals(
        delete_to_do,
        2,
        TO_DO_LISTING = TO_DO_LISTING,
        query_delete_to_do = query_delete_to_do_patched,
    )
    
    await mocked(to_do)
    
    vampytest.assert_eq(TO_DO_LISTING, [])
    vampytest.assert_false(query_delete_to_do_called)
