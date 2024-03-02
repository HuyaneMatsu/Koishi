import vampytest
from hata import Channel, Client, Message, User

from ..reminding import notify_user


async def test__notify_user__success():
    """
    Tests whether ``notify_user`` works as intended.
    
    Case: Success.
    """
    client_id = 202402290012
    channel_id = 202402290013
    user_id = 202402290014
    message_id = 202402290015
    entry_id = 23
    connector = object()
    set_entry_as_notified_with_connector_called = False
    
    channel = Channel.precreate(channel_id)
    user = User.precreate(user_id)
    message = Message.precreate(message_id)
    
    async def get_user(input_user_id):
        nonlocal user
        nonlocal user_id
        vampytest.assert_eq(input_user_id, user_id)
        return user
    
    async def channel_private_create(input_user_id):
        nonlocal channel
        nonlocal user_id
        
        vampytest.assert_eq(input_user_id, user_id)
        return channel
    
    
    async def message_create(input_channel, **keyword_parameters):
        nonlocal channel
        nonlocal message
        
        vampytest.assert_is(input_channel, channel)
        vampytest.assert_eq({*keyword_parameters}, {'allowed_mentions', 'components', 'embed'})
        return message
    
    
    async def set_entry_as_notified_with_connector(input_connector, input_entry_id):
        nonlocal connector
        nonlocal entry_id
        nonlocal set_entry_as_notified_with_connector_called
        vampytest.assert_eq(input_connector, connector)
        vampytest.assert_eq(input_entry_id, entry_id)
        set_entry_as_notified_with_connector_called = True
    
    
    mocked = vampytest.mock_globals(
        notify_user,
        2,
        get_user = get_user,
        set_entry_as_notified_with_connector = set_entry_as_notified_with_connector,
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.channel_private_create = channel_private_create
    client.message_create = message_create
    
    try:
        output = await mocked((entry_id, user_id, client_id), connector)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
        vampytest.assert_true(set_entry_as_notified_with_connector_called)
    
    finally:
        client._delete()
        client = None
