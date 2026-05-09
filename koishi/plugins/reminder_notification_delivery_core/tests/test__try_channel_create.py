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
    
    channel = Channel.precreate(channel_id)
    
    async def channel_private_create(self, input_user_id):
        nonlocal channel
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return channel
    
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    channel_private_create_original = Client.channel_private_create
    Client.channel_private_create = channel_private_create
    
    try:
        output = await try_channel_create(client, user_id)
        vampytest.assert_eq(output, (channel, False))
    
    finally:
        Client.channel_private_create = channel_private_create_original
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
    
    exception = DiscordException(None, None, None, None)
    exception.status = 400
    exception.code = ERROR_CODES.unknown_user
    
    async def channel_private_create(self, input_user_id):
        nonlocal exception
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        raise exception
    
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    channel_private_create_original = Client.channel_private_create
    Client.channel_private_create = channel_private_create
    
    try:
        output = await try_channel_create(client, user_id)
        vampytest.assert_eq(output, (None, True))
    
    finally:
        Client.channel_private_create = channel_private_create_original
        client._delete()
        client = None
