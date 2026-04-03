import vampytest
from hata import Channel, ChannelType, Client, ClientWrapper, Guild, GuildProfile

from ..events import channel_delete


async def test__channel_delete():
    """
    Tests whether ``channel_delete`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202503170092
    channel_id_0 = 202503170093
    guild_id = 202503170098
    
    channel_0 = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_text)
    
    execute_channel_delete_called = False
    
    async def mocked_execute_channel_delete(input_channel):
        nonlocal channel_0
        nonlocal execute_channel_delete_called
        
        vampytest.assert_is(channel_0, input_channel)
        execute_channel_delete_called = True
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    guild = None
    try:
        client.guild_profiles[guild_id] = GuildProfile()
        
        guild = Guild.precreate(
            guild_id,
        )
        
        guild.clients.append(client)
        
        client_wrapper = ClientWrapper(client)
        
        mocked = vampytest.mock_globals(
            channel_delete,
            execute_channel_delete = mocked_execute_channel_delete,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, channel_0)
        
        vampytest.assert_true(execute_channel_delete_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
