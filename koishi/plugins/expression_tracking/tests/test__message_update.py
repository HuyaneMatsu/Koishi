import vampytest
from hata import (
    BUILTIN_EMOJIS, Channel, ChannelType, Client, ClientWrapper, Guild, GuildProfile, Emoji, Message, Permission, Role,
    User
)

from ..events import message_update


async def test__message_update():
    """
    Tests whether ``message_update`` works as intended.
    
    This function is a coroutine.
    """
    message_id = 202503170020
    author_id = 202503170021
    client_id = 202503170022
    emoji_id_0 = 202503170023
    emoji_id_1 = 202503170024
    emoji_id_2 = 202503170025
    channel_id_0 = 202503170027
    guild_id = 202503170028
    role_id_0 = 202503170029
    
    author = User.precreate(author_id)
    
    emoji_0 = Emoji.precreate(emoji_id_0, name = 'KoishiSmile')
    emoji_1 = Emoji.precreate(emoji_id_1, name = 'KoishiHug')
    emoji_2 = Emoji.precreate(emoji_id_2, name = 'KoishiFist')
    emoji_3 = BUILTIN_EMOJIS['heart']
    
    message = Message.precreate(
        message_id,
        author = author,
        channel_id = channel_id_0,
        guild_id = guild_id,
        content = f'{emoji_0}{emoji_2}{emoji_3}',
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
    
    execute_message_update_called = False
    
    async def mocked_execute_message_update(
        input_message, input_delete_old_emojis, input_delete_all_old_emoji, input_add_new_emojis
    ):
        nonlocal message
        nonlocal emoji_1
        nonlocal emoji_2
        nonlocal execute_message_update_called
        
        vampytest.assert_is(message, input_message)
        vampytest.assert_eq(input_delete_old_emojis, {emoji_1})
        vampytest.assert_false(input_delete_all_old_emoji)
        vampytest.assert_eq(input_add_new_emojis, {emoji_2})
        execute_message_update_called = True
    
    
    old_attributes = {
        'content': f'{emoji_0}{emoji_3}{emoji_1}'
    }
    
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
            message_update,
            execute_message_update = mocked_execute_message_update,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, message, old_attributes)
        
        vampytest.assert_true(execute_message_update_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
