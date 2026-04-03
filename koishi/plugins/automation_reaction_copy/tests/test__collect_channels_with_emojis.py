import vampytest
from hata import (
    Channel, ChannelType, BUILTIN_EMOJIS, Guild, GuildProfile, Permission, PermissionOverwrite,
    PermissionOverwriteTargetType, Role, User
)

from ..constants import MASK_PARSE_NAME_ALL, MASK_PARSE_TOPIC_ALL
from ..list_channels import collect_channels_with_emojis


def test__collect_channels_with_emojis__with_match():
    """
    Tests whether ``collect_channels_with_emojis`` works as intended.
    """
    guild_id = 202406100011
    channel_id_0 =  20240610013
    channel_id_1 = 20240610014
    channel_id_2 = 20240610015
    channel_id_3 = 20240610016
    channel_id_4 = 20240610017
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    emoji_2 = BUILTIN_EMOJIS['green_heart']
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        name = f'{emoji_0}',
        topic = f'hey mister {emoji_1}'
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_thread_public,
        parent_id = channel_id_0,
        guild_id = guild_id,
        name = f'{emoji_1}',
    )
    
    channel_2 = Channel.precreate(
        channel_id_2,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        permission_overwrites = [],
        name = f'{emoji_1}',
    )

    channel_3 = Channel.precreate(
        channel_id_3,
        channel_type = ChannelType.guild_category,
        guild_id = guild_id,
    )
    
    channel_4 = Channel.precreate(
        channel_id_4,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        parent_id = channel_id_3,
        name = f'{emoji_2}',
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission().update_by_keys(view_channel = True),
    )
    
    
    guild = Guild.precreate(
        guild_id,
        roles = [role],
        channels = [channel_0, channel_2, channel_3, channel_4],
        threads = [channel_1],
    )
    
    without_category, by_category = collect_channels_with_emojis(guild, MASK_PARSE_NAME_ALL | MASK_PARSE_TOPIC_ALL)
    vampytest.assert_instance(without_category, list, nullable = True)
    vampytest.assert_instance(by_category, list)
    
    vampytest.assert_eq(
        without_category,
        [
            (channel_0, [emoji_0]),
        ],
    )
    
    vampytest.assert_eq(
        by_category,
        [
            (
                channel_3,
                [
                    (channel_4, [emoji_2]),
                ],
            )
        ]
    )
