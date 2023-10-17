import vampytest

from ..constants import BLACKLIST
from ..queries import remove_user_id_from_blacklist_with_connector


async def test__remove_user_id_from_blacklist_with_connector__in():
    """
    Tests whether ``remove_user_id_from_blacklist_with_connector`` works as intended.
    
    This function is a coroutine.
    
    Case: in cache.
    """
    query_called = False
    user_id = 202310170009
    entry_id = 17
    query_called_with_entry_id = 0
    connector = object()
    query_called_with_connector = None
    
    async def query(entry_id, connector):
        nonlocal query_called
        nonlocal query_called_with_entry_id
        nonlocal query_called_with_connector
        
        query_called = True
        query_called_with_entry_id = entry_id
        query_called_with_connector = connector
    
    
    mocked = vampytest.mock_globals(
        remove_user_id_from_blacklist_with_connector,
        _remove_entry_id_from_blacklist_with_connector = query,
    )
    
    try:
        BLACKLIST[user_id] = entry_id
    
        output = await mocked(user_id, connector)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(query_called_with_entry_id, entry_id)
        vampytest.assert_is(query_called_with_connector, connector)
            
        vampytest.assert_eq(BLACKLIST.get(user_id, 0), 0)
    
    finally:
        BLACKLIST.clear()


async def test__remove_user_id_from_blacklist_with_connector__out():
    """
    Tests whether ``remove_user_id_from_blacklist_with_connector`` works as intended.
    
    This function is a coroutine.
    
    Case: out of cache.
    """
    query_called = False
    user_id = 202310170010
    connector = object()
    
    async def query(entry_id, connector):
        nonlocal query_called
        
        query_called = True
    
    
    mocked = vampytest.mock_globals(
        remove_user_id_from_blacklist_with_connector,
        _remove_entry_id_from_blacklist_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
        vampytest.assert_false(query_called)
        
    finally:
        BLACKLIST.clear()
