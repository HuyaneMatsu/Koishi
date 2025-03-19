import vampytest
from hata import Channel, ChannelType, Client, ClientWrapper, Guild, GuildProfile, Message, Permission, Role, User

from ..events import message_delete


async def test__message_delete():
    """
    Tests whether ``message_delete`` works as intended.
    
    This function is a coroutine.
    """
    message_id = 202503170010
    author_id = 202503170011
    client_id = 202503170012
    channel_id_0 = 202503170017
    guild_id = 202503170018
    role_id_0 = 202503170019
    
    author = User.precreate(author_id)
    
    message = Message.precreate(
        message_id,
        author = author,
        channel_id = channel_id_0,
        guild_id = guild_id,
    )
    
    role_0 = Role.precreate(
        role_id_0,
        guild_id = guild_id,
        permissions = Permission().update_by_keys(administrator = True),
    )
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
    )
    
    execute_message_delete_called = False
    
    async def mocked_execute_message_delete(input_message):
        nonlocal message
        nonlocal execute_message_delete_called
        
        vampytest.assert_is(message, input_message)
        execute_message_delete_called = True
    
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    guild = None
    try:
        client.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
        
        guild = Guild.precreate(
            guild_id,
            channels = [channel_0],
            roles = [role_0],
            users = [author, client],
        )
        
        guild.clients.append(client)
        
        client_wrapper = ClientWrapper(client)
        
        mocked = vampytest.mock_globals(
            message_delete,
            execute_message_delete = mocked_execute_message_delete,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, message)
        
        vampytest.assert_true(execute_message_delete_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
