import vampytest

from hata import BUILTIN_EMOJIS, Channel, ChannelType

from ..list_channels import sort_channels_and_emojis


def test__sort_channels_and_emojis():
    """
    Tests whether ``sort_channels_and_emojis`` works as intended.
    """
    channel_id_0 = 202406090010
    channel_id_1 = 202406090011
    channel_id_2 = 202406090012
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        position = 10,
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_text,
        position = 9,
    )
    
    channel_2 = Channel.precreate(
        channel_id_2,
        channel_type = ChannelType.guild_text,
        position = 8,
    )
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    emoji_2 = BUILTIN_EMOJIS['black_heart']
    emoji_3 = BUILTIN_EMOJIS['green_heart']
    emoji_4 = BUILTIN_EMOJIS['pink_heart']
    
    group = [
        (channel_0, [emoji_1, emoji_0]),
        (channel_2, [emoji_2, emoji_3]),
        (channel_1, [emoji_4]),
    ]
    
    sort_channels_and_emojis(group)
    
    vampytest.assert_eq(
        group,
        [
            (channel_2, [emoji_2, emoji_3]),
            (channel_1, [emoji_4]),
            (channel_0, [emoji_1, emoji_0]),
        ],
    )
