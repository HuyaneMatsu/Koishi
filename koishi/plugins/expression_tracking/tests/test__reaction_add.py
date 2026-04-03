import vampytest
from hata import (
    Channel, ChannelType, Client, ClientWrapper, Guild, GuildProfile, Emoji, Message, Permission, ReactionAddEvent,
    Role, User
)

from ..events import reaction_add


async def test__reaction_add():
    """
    Tests whether ``reaction_add`` works as intended.
    
    This function is a coroutine.
    """
    message_id = 202503170030
    author_id = 202503170031
    client_id = 202503170032
    emoji_id_0 = 202503170033
    user_id_0 = 202503170034
    channel_id_0 = 202503170037
    guild_id = 202503170038
    role_id_0 = 202503170039
    
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
    
    execute_reaction_add_called = False
    
    async def mocked_execute_reaction_add(input_message, input_emoji, input_user):
        nonlocal message
        nonlocal emoji_0
        nonlocal user_0
        nonlocal execute_reaction_add_called
        
        vampytest.assert_is(message, input_message)
        vampytest.assert_is(input_emoji, emoji_0)
        vampytest.assert_is(input_user, user_0)
        execute_reaction_add_called = True
    
    event = ReactionAddEvent(message, emoji_0, user_0)
    
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
            reaction_add,
            execute_reaction_add = mocked_execute_reaction_add,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, event)
        
        vampytest.assert_true(execute_reaction_add_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
