import vampytest

from hata import BUILTIN_EMOJIS, Channel, ChannelType

from ..list_channels import filter_emojis_to_channels


def test__filter_emojis_to_channels():
    """
    Tests whether ``filter_emojis_to_channels`` works as intended.
    """
    channel_0 = Channel.precreate(
        202406090000,
        channel_type = ChannelType.guild_text,
    )
    
    channel_1 = Channel.precreate(
        202406090001,
        channel_type = ChannelType.guild_text,
    )
    
    channel_2 = Channel.precreate(
        202406090002,
        channel_type = ChannelType.guild_text,
    )
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    emoji_2 = BUILTIN_EMOJIS['black_heart']
    emoji_3 = BUILTIN_EMOJIS['green_heart']
    
    emojis_to_channels = {
        emoji_0: [channel_0, channel_1],
        emoji_1: [channel_2],
        emoji_2: [channel_0],
        emoji_3: [channel_0],
    }
    
    output = filter_emojis_to_channels(emojis_to_channels)
    vampytest.assert_instance(output, dict)
    
    vampytest.assert_eq(
        output,
        {
            channel_2: [emoji_1],
            channel_0: [emoji_2, emoji_3],
        },
    )
