import vampytest
from hata import DiscordException, ERROR_CODES, User

from ..requests import try_user_get


async def test__try_user_get__success():
    """
    Tests whether ``try_user_get`` works as intended.
    
    Case: Success.
    
    This function is a coroutine.
    """
    user_id = 202402280001
    entry_id = 23
    connector = object()
    
    user = User.precreate(user_id)
    
    async def get_user(input_user_id):
        nonlocal user
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return user
    
    
    async def set_entry_as_notified_with_connector(input_connector, input_entry_id):
        raise RuntimeError('Should not been called')
    
    
    mocked = vampytest.mock_globals(
        try_user_get,
        get_user = get_user,
        set_entry_as_notified_with_connector = set_entry_as_notified_with_connector,
    )
    
    output = await mocked(user_id, entry_id, connector)
    vampytest.assert_is(output, user)


async def test__try_user_get__deleted():
    """
    Tests whether ``try_user_get`` works as intended.
    
    Case: User deleted.
    
    This function is a coroutine.
    """
    user_id = 202402280002
    entry_id = 23
    connector = object()
    set_entry_as_notified_with_connector_called = False
    
    exception = DiscordException(None, None, None, None)
    exception.status = 400
    exception.code = ERROR_CODES.unknown_user
    
    async def get_user(input_user_id):
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        nonlocal exception
        raise exception
    
    
    async def set_entry_as_notified_with_connector(input_connector, input_entry_id):
        nonlocal connector
        nonlocal entry_id
        nonlocal set_entry_as_notified_with_connector_called
        vampytest.assert_eq(input_connector, connector)
        vampytest.assert_eq(input_entry_id, entry_id)
        set_entry_as_notified_with_connector_called = True
    
    
    mocked = vampytest.mock_globals(
        try_user_get,
        get_user = get_user,
        set_entry_as_notified_with_connector = set_entry_as_notified_with_connector,
    )
    
    output = await mocked(user_id, entry_id, connector)
    vampytest.assert_is(output, None)
    vampytest.assert_true(set_entry_as_notified_with_connector_called)
