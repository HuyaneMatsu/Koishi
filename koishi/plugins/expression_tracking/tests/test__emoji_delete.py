import vampytest
from hata import Client, ClientWrapper, Guild, GuildProfile, Emoji

from ..events import emoji_delete


async def test__emoji_delete():
    """
    Tests whether ``emoji_delete`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202503170072
    emoji_id_0 = 202503170073
    guild_id = 202503170078
    
    emoji_0 = Emoji.precreate(emoji_id_0, name = 'KoishiSmile')
    
    execute_emoji_delete_called = False
    
    async def mocked_execute_emoji_delete(input_emoji):
        nonlocal emoji_0
        nonlocal execute_emoji_delete_called
        
        vampytest.assert_is(emoji_0, input_emoji)
        execute_emoji_delete_called = True
    
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
            emoji_delete,
            execute_emoji_delete = mocked_execute_emoji_delete,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, emoji_0)
        
        vampytest.assert_true(execute_emoji_delete_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
