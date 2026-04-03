import vampytest
from hata import Channel, ChannelType, BUILTIN_EMOJIS, Guild

from ..constants import MASK_PARSE_NAME_UNICODE, MASK_PARSE_TOPIC_CUSTOM, MASK_PARSE_TOPIC_UNICODE
from ..events import try_get_target_channel


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    
    guild_id = 202406120007
    
    guild = Guild.precreate(
        guild_id,
        channels = [],
        threads = [],
    )

    yield guild, emoji_0, 0, None
    yield guild, emoji_0, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, None
    
    
    guild_id = 202406120009
    channel_id_0 = 202406120010
    channel_id_1 = 202406120011
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        name = 'orin',
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_thread_public,
        guild_id = guild_id,
        name = 'miau',
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel_0],
        threads = [channel_1],
    )
    
    yield guild, emoji_0, 0, None
    yield guild, emoji_0, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, None
    yield guild, emoji_1, 0, None
    yield guild, emoji_1, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, None
    
    
    guild_id = 202406120012
    channel_id_0 = 202406120013
    channel_id_1 = 202406120014
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        name = emoji_0.as_emoji,
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_thread_public,
        guild_id = guild_id,
        name = 'miau',
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel_0],
        threads = [channel_1],
    )
    
    yield guild, emoji_0, 0, None
    yield guild, emoji_0, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, channel_0
    yield guild, emoji_1, 0, None
    yield guild, emoji_1, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, None
    
    
    guild_id = 202406120015
    channel_id_0 = 202406120016
    channel_id_1 = 202406120017
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        name = 'orin',
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_thread_public,
        guild_id = guild_id,
        name = emoji_0.as_emoji,
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel_0],
        threads = [channel_1],
    )
    
    yield guild, emoji_0, 0, None
    yield guild, emoji_0, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, channel_1
    yield guild, emoji_1, 0, None
    yield guild, emoji_1, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, None
    
    
    guild_id = 202406120018
    channel_id_0 = 202406120019
    channel_id_1 = 202406120020
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        name = emoji_0.as_emoji,
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_thread_public,
        guild_id = guild_id,
        name = emoji_0.as_emoji,
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel_0],
        threads = [channel_1],
    )
    
    yield guild, emoji_0, 0, None
    yield guild, emoji_0, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, None
    yield guild, emoji_1, 0, None
    yield guild, emoji_1, MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE, None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__try_get_target_channel(guild, emoji, flags):
    """
    Tests whether ``try_get_target_channel`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild where reaction was added at.
    emoji : ``Emoji``
        The emoji to check for.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    output : `None | Channel`
    """
    output = try_get_target_channel(guild, emoji, flags)
    vampytest.assert_instance(output, Channel, nullable = True)
    return output
