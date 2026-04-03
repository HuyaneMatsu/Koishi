import vampytest
from hata import (
    Channel, ChannelType, Client, ClientWrapper, Guild, GuildProfile, Emoji, Message, Permission, Reaction,
    ReactionMapping, ReactionMappingLine, Role, User
)

from ..events import reaction_clear


async def test__reaction_clear():
    """
    Tests whether ``reaction_clear`` works as intended.
    
    This function is a coroutine.
    """
    message_id = 202503170060
    author_id = 202503170061
    client_id = 202503170062
    emoji_id_0 = 202503170063
    user_id_0 = 202503170064
    channel_id_0 = 202503170067
    guild_id = 202503170068
    role_id_0 = 202503170069
    
    author = User.precreate(author_id)
    user_0 = User.precreate(user_id_0)
    
    emoji_0 = Emoji.precreate(emoji_id_0, name = 'KoishiSmile')
    
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
    
    execute_reaction_clear_called = False
    
    async def mocked_execute_reaction_clear(input_message):
        nonlocal message
        nonlocal execute_reaction_clear_called
        
        vampytest.assert_is(message, input_message)
        execute_reaction_clear_called = True
    
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
            users = [author, client, user_0],
        )
        
        guild.clients.append(client)
        
        client_wrapper = ClientWrapper(client)
        
        mocked = vampytest.mock_globals(
            reaction_clear,
            execute_reaction_clear = mocked_execute_reaction_clear,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(
            client,
            message,
            ReactionMapping(lines = {Reaction(emoji_0): ReactionMappingLine(users = [user_0])}),
        )
        
        vampytest.assert_true(execute_reaction_clear_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
