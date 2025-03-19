import vampytest
from hata import (
    BUILTIN_EMOJIS, Channel, ChannelType, Client, ClientWrapper, Guild, GuildProfile, Emoji, Message, Permission, Role,
    Sticker, StickerType, User
)

from ..events import message_create


async def test__message_create():
    """
    Tests whether ``message_create`` works as intended.
    
    This function is a coroutine.
    """
    message_id = 202503170000
    author_id = 202503170001
    client_id = 202503170002
    emoji_id_0 = 202503170003
    emoji_id_1 = 202503170004
    sticker_id_0 = 202503170005
    sticker_id_1 = 202503170006
    channel_id_0 = 202503170007
    guild_id = 202503170008
    role_id_0 = 202503170009
    
    author = User.precreate(author_id)
    
    emoji_0 = Emoji.precreate(emoji_id_0, name = 'KoishiSmile')
    emoji_1 = Emoji.precreate(emoji_id_1, name = 'KoishiHug')
    emoji_2 = BUILTIN_EMOJIS['heart']
    
    sticker_0 = Sticker.precreate(sticker_id_0, name = 'KoishiHappy', sticker_type = StickerType.guild)
    sticker_1 = Sticker.precreate(sticker_id_1, name = 'CringeStuff', sticker_type = StickerType.standard)
    
    message = Message.precreate(
        message_id,
        author = author,
        channel_id = channel_id_0,
        guild_id = guild_id,
        content = f'{emoji_0}{emoji_1}{emoji_2}{emoji_1}',
        stickers = [sticker_0, sticker_0, sticker_1],
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
    
    execute_message_create_called = False
    
    async def mocked_execute_message_create(input_message, input_custom_emojis, input_stickers):
        nonlocal message
        nonlocal emoji_0
        nonlocal emoji_1
        nonlocal sticker_0
        nonlocal execute_message_create_called
        
        vampytest.assert_is(message, input_message)
        vampytest.assert_eq(input_custom_emojis, {emoji_0, emoji_1})
        vampytest.assert_eq(input_stickers, {sticker_0})
        execute_message_create_called = True
    
    
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
            message_create,
            execute_message_create = mocked_execute_message_create,
            FEATURE_CLIENTS = client_wrapper,
        )
        
        await mocked(client, message)
        
        vampytest.assert_true(execute_message_create_called)
    
    finally:
        if (guild is not None):
            guild._delete(client)
            guild = None
        
        client._delete()
        client = None
