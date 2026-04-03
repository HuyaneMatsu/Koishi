import vampytest
from hata import Channel, Client, DiscordException, ERROR_CODES

from ..requests import try_channel_create


async def test__try_channel_create__success():
    """
    Tests whether ``try_channel_create`` works as intended.
    
    Case: Success.
    
    This function is a coroutine.
    """
    user_id = 202402290000
    client_id = 202402290001
    channel_id = 202402290002
    entry_id = 23
    connector = object()
    
    channel = Channel.precreate(channel_id)
    
    async def channel_private_create(input_user_id):
        nonlocal channel
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return channel
    
    
    async def set_entry_as_notified_with_connector(input_connector, input_entry_id):
        raise RuntimeError('Should not been called')
    
    
    mocked = vampytest.mock_globals(
        try_channel_create,
        set_entry_as_notified_with_connector = set_entry_as_notified_with_connector,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.channel_private_create = channel_private_create
    
    try:
        output = await mocked(client, user_id, entry_id, connector)
        vampytest.assert_is(output, channel)
    
    finally:
        client._delete()
        client = None


async def test__try_channel_create__deleted():
    """
    Tests whether ``try_channel_create`` works as intended.
    
    Case: User deleted.
    
    This function is a coroutine.
    """
    user_id = 202402290003
    client_id = 202402290004
    entry_id = 23
    connector = object()
    set_entry_as_notified_with_connector_called = False
    
    exception = DiscordException(None, None, None, None)
    exception.status = 400
    exception.code = ERROR_CODES.unknown_user
    
    async def channel_private_create(input_user_id):
        nonlocal exception
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        raise exception
    
    
    async def set_entry_as_notified_with_connector(input_connector, input_entry_id):
        nonlocal connector
        nonlocal entry_id
        nonlocal set_entry_as_notified_with_connector_called
        vampytest.assert_eq(input_connector, connector)
        vampytest.assert_eq(input_entry_id, entry_id)
        set_entry_as_notified_with_connector_called = True
    
    
    mocked = vampytest.mock_globals(
        try_channel_create,
        set_entry_as_notified_with_connector = set_entry_as_notified_with_connector,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.channel_private_create = channel_private_create
    
    try:
        output = await mocked(client, user_id, entry_id, connector)
        vampytest.assert_is(output, None)
        vampytest.assert_true(set_entry_as_notified_with_connector_called)
    
    finally:
        client._delete()
        client = None
