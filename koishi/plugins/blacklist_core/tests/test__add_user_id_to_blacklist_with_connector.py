import vampytest

from ..constants import BLACKLIST
from ..queries import add_user_id_to_blacklist_with_connector


async def test__add_user_id_to_blacklist_with_connector__in():
    """
    Tests whether ``add_user_id_to_blacklist_with_connector`` works as intended.
    
    This function is a coroutine.
    
    Case: in cache.
    """
    query_called = False
    user_id = 202310170003
    entry_id = 17
    connector = object()
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal entry_id
        
        query_called = True
        return entry_id
    
    
    mocked = vampytest.mock_globals(
        add_user_id_to_blacklist_with_connector,
        _add_user_id_to_blacklist_with_connector = query,
    )
    
    try:
        BLACKLIST[user_id] = entry_id
    
        output = await mocked(user_id, connector)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
        
        vampytest.assert_false(query_called)
        
    finally:
        BLACKLIST.clear()


async def test__add_user_id_to_blacklist_with_connector__out():
    """
    Tests whether ``add_user_id_to_blacklist_with_connector`` works as intended.
    
    This function is a coroutine.
    
    Case: out of cache.
    """
    query_called = False
    user_id = 202310170004
    entry_id = 17
    query_called_user_id = 0
    connector = object()
    query_called_with_connector = None
    
    
    async def query(user_id, connector):
        nonlocal query_called
        nonlocal query_called_user_id
        nonlocal entry_id
        nonlocal query_called_with_connector
        
        query_called = True
        query_called_user_id = user_id
        query_called_with_connector = connector
        return entry_id
    
    
    mocked = vampytest.mock_globals(
        add_user_id_to_blacklist_with_connector,
        _add_user_id_to_blacklist_with_connector = query,
    )
    
    try:
        output = await mocked(user_id, connector)
        
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(query_called_user_id, user_id)
        vampytest.assert_is(query_called_with_connector, connector)
        
        vampytest.assert_eq(BLACKLIST.get(user_id, 0), entry_id)
        
    finally:
        BLACKLIST.clear()
