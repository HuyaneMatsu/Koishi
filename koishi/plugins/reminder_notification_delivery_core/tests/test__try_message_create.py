import vampytest
from hata import Channel, Client, ComponentType, Component, DiscordException, ERROR_CODES, Message

from ..requests import try_message_create


async def test__try_message_create__success():
    """
    Tests whether ``try_message_create`` works as intended.
    
    Case: Success.
    
    This function is a coroutine.
    """
    message_id = 202402290006
    client_id = 202402290007
    channel_id = 202402290008
    
    channel = Channel.precreate(channel_id)
    message = Message.precreate(message_id)
    
    components = [
        Component(
            component_type = ComponentType.button,
            label = 'hey',
            custom_id = 'mister',
        ),
    ]
    
    async def message_create(self, input_channel, **keyword_parameters):
        nonlocal channel
        nonlocal components
        nonlocal message
        
        vampytest.assert_is(input_channel, channel)
        vampytest.assert_eq(
            keyword_parameters,
            {
                'allowed_mentions': None,
                'components': components,
            },
        )
        
        return message
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    message_create_original = Client.message_create
    Client.message_create = message_create
    
    try:
        output = await try_message_create(client, channel, components)
        vampytest.assert_eq(output, (message, False))
    
    finally:
        Client.message_create = message_create_original
        client._delete()
        client = None


async def test__try_message_create__cannot_message_user():
    """
    Tests whether ``try_message_create`` works as intended.
    
    Case: User cannot be messaged.
    
    This function is a coroutine.
    """
    client_id = 202402290010
    channel_id = 202402290011
    
    channel = Channel.precreate(channel_id)
    
    components = [
        Component(
            component_type = ComponentType.button,
            label = 'hey',
            custom_id = 'mister',
        ),
    ]
    
    exception = DiscordException(None, None, None, None)
    exception.status = 400
    exception.code = ERROR_CODES.cannot_message_user_0
    
    async def message_create(self, input_channel, **keyword_parameters):
        nonlocal channel
        nonlocal components
        nonlocal exception
        
        vampytest.assert_is(input_channel, channel)
        vampytest.assert_eq(
            keyword_parameters,
            {
                'allowed_mentions': None,
                'components': components,
            },
        )
        
        raise exception
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    message_create_original = Client.message_create
    Client.message_create = message_create
    
    try:
        output = await try_message_create(client, channel, components)
        vampytest.assert_eq(output, (None, True))
    
    finally:
        Client.message_create = message_create_original
        client._delete()
        client = None
