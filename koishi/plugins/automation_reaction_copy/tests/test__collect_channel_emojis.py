import vampytest
from hata import Channel, ChannelType, BUILTIN_EMOJIS, Emoji

from ..constants import MASK_PARSE_NAME_UNICODE, MASK_PARSE_TOPIC_CUSTOM, MASK_PARSE_TOPIC_UNICODE
from ..list_channels import collect_channel_emojis


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
        0,
        set(),
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = 'pudding',
            topic = None,
        ),
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        set(),
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        0,
        set(),
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        MASK_PARSE_NAME_UNICODE | MASK_PARSE_TOPIC_CUSTOM | MASK_PARSE_TOPIC_UNICODE,
        {emoji_0, emoji_1, emoji_3},
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        MASK_PARSE_NAME_UNICODE,
        {emoji_0},
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        MASK_PARSE_TOPIC_CUSTOM,
        {emoji_3},
    )
    
    yield (
        Channel(
            channel_type = ChannelType.guild_text,
            name = f'pudding {emoji_0} {emoji_2}',
            topic = f'{emoji_1} {emoji_3}',
        ),
        MASK_PARSE_TOPIC_UNICODE,
        {emoji_1},
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__collect_channel_emojis(channel, flags):
    """
    Tests whether ``collect_channel_emojis`` works as intended.
    
    Parameters
    ----------
    channel : ``Channel``
        Channel to collect the emojis of.
    flags : `int`
        Bitwise flags to determine from where and what kind of emojis should we collect.
    
    Returns
    -------
    output : `set<Emoji>`
    """
    output = collect_channel_emojis(channel, flags)
    
    vampytest.assert_instance(output, set)
    for element in output:
        vampytest.assert_instance(element, Emoji)
    
    return output
