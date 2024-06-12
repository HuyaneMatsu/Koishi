import vampytest
from hata import Channel, ChannelType, BUILTIN_EMOJIS, Emoji

from ..constants import MASK_PARSE_NAME_UNICODE, MASK_PARSE_TOPIC_CUSTOM, MASK_PARSE_TOPIC_UNICODE
from ..events import check_has_channel_emoji


def _iter_options():
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    emoji_2 = Emoji.precreate(202406080000, name = 'koishi')
    emoji_3 = Emoji.precreate(202406080001, name = 'satori')


    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = 'pudding',
            topic = None,
        ),
        emoji_0,
        0,
        False,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = 'pudding',
            topic = None,
        ),
        emoji_0,
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        False,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_0,
        0,
        False,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_0,
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        True,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_1,
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        True,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_2,
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        False,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_3,
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        True,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_0,
        MASK_PARSE_NAME_UNICODE,
        True,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_3,
        MASK_PARSE_TOPIC_CUSTOM,
        True,
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        emoji_1,
        MASK_PARSE_TOPIC_UNICODE,
        True,
    )



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_has_channel_emoji(channel, emoji, flags):
    """
    Tests whether ``check_has_channel_emoji`` works as intended.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to collect the emojis of.
    emoji : ``Emoji``
        The emoji to check for.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    output : `bool`
    """
    output = check_has_channel_emoji(channel, emoji, flags)
    vampytest.assert_instance(output, bool)
    return output

