import vampytest

from ..cache import USER_SETTINGS_CACHE, put_one_to_cache
from ..user_settings import UserSettings
from ..queries import get_more_user_settings_with_connector


async def test__get_more_user_settings_with_connector__cache_hit():
    """
    Tests whether ``get_more_user_settings_with_connector`` works as intended.
    
    Case: Cache hit.
    
    This function is a coroutine.
    """
    query_called = False
    connector = object()
    
    user_id_0 = 202309250070
    user_id_1 = 202309250071
    
    user_settings_0 = UserSettings(user_id_0, notification_daily_by_waifu = False)
    user_settings_1 = UserSettings(user_id_1, notification_proposal = False)
    
    async def query(user_ids, connector):
        nonlocal query_called
        query_called = True
        
        return None, None
    
    
    mocked = vampytest.mock_globals(
        get_more_user_settings_with_connector,
        _query_more_user_settings_with_connector = query,
    )
    
    try:
        put_one_to_cache(user_settings_0)
        put_one_to_cache(user_settings_1)
        
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_eq(output, [user_settings_0, user_settings_1])
        
        vampytest.assert_false(query_called)
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__get_more_user_settings_with_connector__database_hit_value():
    """
    Tests whether ``get_more_user_settings_with_connector`` works as intended.
    
    Case: Database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = None
    connector = object()
    called_with_connector = None
    
    user_id_0 = 202309250072
    user_id_1 = 202309250073
    
    user_settings_0 = UserSettings(user_id_0, notification_daily_by_waifu = False)
    user_settings_1 = UserSettings(user_id_1, notification_proposal = False)
    
    async def query(user_ids, connector):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal user_settings_0
        nonlocal user_settings_1
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_ids = user_ids
        called_with_connector = connector
        
        return [user_settings_0, user_settings_1], None
    
    
    mocked = vampytest.mock_globals(
        get_more_user_settings_with_connector,
        _query_more_user_settings_with_connector = query,
    )
    
    try:
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_eq(output, [user_settings_0, user_settings_1])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_0, user_id_1])
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_0, user_settings_0), (user_id_1, user_settings_1)],
        )
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__get_more_user_settings_with_connector__database_hit_none():
    """
    Tests whether ``get_more_user_settings_with_connector`` works as intended.
    
    Case: Database hit with none.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = 0
    connector = object()
    called_with_connector = None
    
    user_id_0 = 202309250074
    user_id_1 = 202309250075
    
    async def query(user_ids, connector):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal user_id_0
        nonlocal user_id_1
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_ids = user_ids
        called_with_connector = connector
        
        return None, [user_id_0, user_id_1]
    
    
    mocked = vampytest.mock_globals(
        get_more_user_settings_with_connector,
        _query_more_user_settings_with_connector = query,
    )
    
    try:
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_eq(output, [UserSettings(user_id_0), UserSettings(user_id_1)])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_0, user_id_1])
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_0, None), (user_id_1, None)],
        )
    finally:
        USER_SETTINGS_CACHE.clear()


async def test__get_more_user_settings_with_connector__mixed_hit_value():
    """
    Tests whether ``get_more_user_settings_with_connector`` works as intended.
    
    Case: Cache and database hit with value.
    
    This function is a coroutine.
    """
    query_called = False
    called_with_user_ids = None
    connector = object()
    called_with_connector = None
    
    user_id_0 = 202309250076
    user_id_1 = 202309250077
    
    user_settings_0 = UserSettings(user_id_0, notification_daily_by_waifu = False)
    user_settings_1 = UserSettings(user_id_1, notification_proposal = False)
    
    async def query(user_ids, connector):
        nonlocal query_called
        nonlocal called_with_user_ids
        nonlocal user_settings_1
        nonlocal called_with_connector
        
        query_called = True
        called_with_user_ids = user_ids
        called_with_connector = connector
        
        return [user_settings_1], None
    
    
    mocked = vampytest.mock_globals(
        get_more_user_settings_with_connector,
        _query_more_user_settings_with_connector = query,
    )
    
    try:
        put_one_to_cache(user_settings_0)
        
        output = await mocked([user_id_0, user_id_1], connector)
        
        vampytest.assert_eq(output, [user_settings_0, user_settings_1])
        
        vampytest.assert_true(query_called)
        vampytest.assert_eq(called_with_user_ids, [user_id_1])
        vampytest.assert_is(called_with_connector, connector)
        
        vampytest.assert_eq(
            [*USER_SETTINGS_CACHE.items()],
            [(user_id_0, user_settings_0), (user_id_1, user_settings_1)],
        )
    finally:
        USER_SETTINGS_CACHE.clear()
