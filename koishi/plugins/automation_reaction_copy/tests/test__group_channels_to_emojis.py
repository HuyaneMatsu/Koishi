import vampytest

from hata import BUILTIN_EMOJIS, Channel, ChannelType

from ..list_channels import group_channels_to_emojis


def test__group_channels_to_emojis():
    """
    Tests whether ``group_channels_to_emojis`` works as intended.
    """
    channel_id_0 = 202406090003
    channel_id_1 = 202406090004
    channel_id_2 = 202406090005
    channel_id_3 = 202406090006
    channel_id_4 = 202406090007
    channel_id_5 = 202406090008
    channel_id_6 = 202406090009
    
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
        channel_type = ChannelType.guild_category,
        position = 8,
    )
    
    channel_3 = Channel.precreate(
        channel_id_3,
        channel_type = ChannelType.guild_text,
        parent_id = channel_id_2,
        position = 7,
    )
    
    channel_4 = Channel.precreate(
        channel_id_4,
        channel_type = ChannelType.guild_text,
        parent_id = channel_id_2,
        position = 6,
    )
    
    channel_5 = Channel.precreate(
        channel_id_5,
        channel_type = ChannelType.guild_category,
        position = 5,
    )
    
    channel_6 = Channel.precreate(
        channel_id_6,
        channel_type = ChannelType.guild_text,
        parent_id = channel_id_5,
        position = 4,
    )
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    emoji_2 = BUILTIN_EMOJIS['black_heart']
    emoji_3 = BUILTIN_EMOJIS['green_heart']
    emoji_4 = BUILTIN_EMOJIS['pink_heart']
    
    channels_to_emojis = {
        channel_0: [emoji_0],
        channel_1: [emoji_1],
        channel_3: [emoji_2],
        channel_4: [emoji_3],
        channel_6: [emoji_4],
    }
    
    without_category, by_category = group_channels_to_emojis(channels_to_emojis)
    vampytest.assert_instance(without_category, list, nullable = True)
    vampytest.assert_instance(by_category, list)
    
    vampytest.assert_eq(
        without_category,
        [
            (channel_1, [emoji_1]),
            (channel_0, [emoji_0]),
        ],
    )

    vampytest.assert_eq(
        by_category,
        [
            (
                channel_5,
                [
                    (channel_6, [emoji_4]),
                ],
            ),
            (
                channel_2,
                [
                    (channel_4, [emoji_3]),
                    (channel_3, [emoji_2]),
                ],
            ),
        ],
    )
