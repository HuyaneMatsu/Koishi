import vampytest
from hata import Channel, Client, ComponentType, Component, DiscordException, ERROR_CODES, Embed, Message

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
    entry_id = 23
    connector = object()
    
    channel = Channel.precreate(channel_id)
    message = Message.precreate(message_id)
    
    embed = Embed('hey', 'mister')
    components = Component(
        component_type = ComponentType.button,
        label = 'hey',
        custom_id = 'mister',
    )
    
    async def message_create(input_channel, **keyword_parameters):
        nonlocal channel
        nonlocal embed
        nonlocal components
        nonlocal message
        
        vampytest.assert_is(input_channel, channel)
        vampytest.assert_eq(
            keyword_parameters,
            {
                'allowed_mentions': None,
                'components': components,
                'embed': embed,
            },
        )
        
        return message
    
    
    async def set_entry_as_notified_with_connector(input_connector, input_entry_id):
        raise RuntimeError('Should not been called')
    
    
    mocked = vampytest.mock_globals(
        try_message_create,
        set_entry_as_notified_with_connector = set_entry_as_notified_with_connector,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.message_create = message_create
    
    try:
        output = await mocked(client, channel, embed, components, entry_id, connector)
        vampytest.assert_is(output, message)
    
    finally:
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
    entry_id = 23
    connector = object()
    set_entry_as_notified_with_connector_called = False
    
    channel = Channel.precreate(channel_id)
    
    embed = Embed('hey', 'mister')
    components = Component(
        component_type = ComponentType.button,
        label = 'hey',
        custom_id = 'mister',
    )
    
    
    exception = DiscordException(None, None, None, None)
    exception.status = 400
    exception.code = ERROR_CODES.cannot_message_user
    
    async def message_create(input_channel, **keyword_parameters):
        nonlocal channel
        nonlocal embed
        nonlocal components
        nonlocal exception
        
        vampytest.assert_is(input_channel, channel)
        vampytest.assert_eq(
            keyword_parameters,
            {
                'allowed_mentions': None,
                'components': components,
                'embed': embed,
            },
        )
        
        raise exception
    
    
    async def set_entry_as_notified_with_connector(input_connector, input_entry_id):
        nonlocal connector
        nonlocal entry_id
        nonlocal set_entry_as_notified_with_connector_called
        vampytest.assert_eq(input_connector, connector)
        vampytest.assert_eq(input_entry_id, entry_id)
        set_entry_as_notified_with_connector_called = True
    
    
    mocked = vampytest.mock_globals(
        try_message_create,
        set_entry_as_notified_with_connector = set_entry_as_notified_with_connector,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.message_create = message_create
    
    try:
        output = await mocked(client, channel, embed, components, entry_id, connector)
        vampytest.assert_is(output, None)
        vampytest.assert_true(set_entry_as_notified_with_connector_called)
    
    finally:
        client._delete()
        client = None
