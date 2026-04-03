import vampytest
from hata import (
    Channel, ChannelType, BUILTIN_EMOJIS, Guild, GuildProfile, Permission, PermissionOverwrite,
    PermissionOverwriteTargetType, Role, User
)

from ..constants import MASK_PARSE_NAME_ALL, MASK_PARSE_TOPIC_ALL
from ..list_channels import collect_emojis_to_channels


def test__collect_emojis_to_channels():
    """
    Tests whether ``collect_emojis_to_channels`` works as intended.
    """
    guild_id = 202406080002
    channel_id_0 =  20240608004
    channel_id_1 = 20240608005
    channel_id_2 = 20240608006
    channel_id_3 = 20240608007
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    
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
        name = f'{emoji_0}',
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission().update_by_keys(view_channel = True),
    )
    
    guild = Guild.precreate(
        guild_id,
        roles = [role],
        channels = [channel_0, channel_1, channel_2, channel_3],
    )
    
    output = collect_emojis_to_channels(guild, MASK_PARSE_NAME_ALL | MASK_PARSE_TOPIC_ALL)
    vampytest.assert_instance(output, dict)
    
    vampytest.assert_eq(
        output,
        {
            emoji_0: [channel_0],
            emoji_1: [channel_0, channel_1, channel_2],
        },
    )
