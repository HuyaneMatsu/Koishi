import vampytest
from hata import Client, ClientWrapper, Guild, GuildProfile

from ..events import guild_delete


async def test__guild_delete():
    """
    Tests whether ``guild_delete`` works as intended.
    
    This function is a coroutine.
    """
    client_id = 202503170102
    guild_id = 202503170108
    
    execute_guild_delete_called = False
    
    async def mocked_execute_guild_delete(input_guild):
        nonlocal guild
        nonlocal execute_guild_delete_called
        
        vampytest.assert_is(guild, input_guild)
        execute_guild_delete_called = True
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    guild = None
    try:
        guild_profile = GuildProfile()
        client.guild_profiles[guild_id] = guild_profile
        
        guild = Guild.precreate(
            guild_id,
        )
        
        client_wrapper = ClientWrapper(client)
        
        mocked = vampytest.mock_globals(
            guild_delete,
            execute_guild_delete = mocked_execute_guild_delete,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, guild, guild_profile)
        
        vampytest.assert_true(execute_guild_delete_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
