import vampytest
from hata import (
    Channel, ChannelType, Client, BUILTIN_EMOJIS, Embed, Guild, GuildProfile, Permission, PermissionOverwrite,
    PermissionOverwriteTargetType, Role
)
from hata.ext.slash import InteractionResponse

from ..constants import COMPONENTS, MASK_PARSE_NAME_ALL, MASK_PARSE_TOPIC_ALL
from ..list_channels import build_reaction_copy_list_channels_response


def test__build_reaction_copy_list_channels_response__with_match():
    """
    Tests whether ``build_reaction_copy_list_channels_response`` works as intended.
    
    Case: with match.
    """
    guild_id = 202406100007
    client_id = 202406100008
    channel_id_0 =  20240610002
    channel_id_1 = 20240610003
    channel_id_2 = 20240610004
    channel_id_3 = 20240610005
    channel_id_4 = 20240610006
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    emoji_2 = BUILTIN_EMOJIS['green_heart']
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        permission_overwrites = [
            PermissionOverwrite(client_id, target_type = PermissionOverwriteTargetType.user, allow = 8),
        ],
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
        permission_overwrites = [
            PermissionOverwrite(client_id, target_type = PermissionOverwriteTargetType.user, allow = 8),
        ],
        name = f'{emoji_1}',
    )

    channel_3 = Channel.precreate(
        channel_id_3,
        channel_type = ChannelType.guild_category,
        guild_id = guild_id,
        name = 'mister',
    )
    
    channel_4 = Channel.precreate(
        channel_id_4,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        parent_id = channel_id_3,
        permission_overwrites = [
            PermissionOverwrite(client_id, target_type = PermissionOverwriteTargetType.user, allow = 8),
        ],
        name = f'{emoji_2}',
    )
    
    role = Role.precreate(
        guild_id,
        permissions = Permission().update_by_keys(view_channel = True),
    )
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(
        guild_id,
        roles = [role],
        channels = [channel_0, channel_1, channel_2, channel_3, channel_4],
        users = [client],
        name = 'sister'
    )
    guild.clients.append(client)
    
    try:
        output = build_reaction_copy_list_channels_response(guild, False, MASK_PARSE_NAME_ALL | MASK_PARSE_TOPIC_ALL)
        vampytest.assert_instance(output, InteractionResponse)
        
        vampytest.assert_eq(
            output,
            InteractionResponse(
                components = COMPONENTS,
                embed = Embed(
                    'sister\'s reaction-copy channels',
                    'Parsing: unicode in name, all in topic.',
                ).add_field(
                    '\u200b',
                    f'{channel_0.mention} : {emoji_0} \\:heart\\:',
                ).add_field(
                    'mister',
                    f'{channel_4.mention} : {emoji_2} \\:green\\_heart\\:',
                ).add_thumbnail(
                    guild.icon_url,
                ).add_footer(
                    '!! Reaction-copy is disabled in the guild !!',
                ),
            ),
        )
    finally:
        client._delete()
        client = None


def test__build_reaction_copy_list_channels_response__no_match():
    """
    Tests whether ``build_reaction_copy_list_channels_response`` works as intended.
    
    Case: no match.
    """
    guild_id = 202406100009
    client_id = 202406100010
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    
    guild = Guild.precreate(
        guild_id,
        users = [client],
        name = 'sister',
    )
    guild.clients.append(client)
    
    try:
        output = build_reaction_copy_list_channels_response(guild, True, MASK_PARSE_NAME_ALL | MASK_PARSE_TOPIC_ALL)
        vampytest.assert_instance(output, InteractionResponse)
        
        vampytest.assert_eq(
            output,
            InteractionResponse(
                components = COMPONENTS,
                embed = Embed(
                    'sister\'s reaction-copy channels',
                    'Parsing: unicode in name, all in topic.',
                ).add_field(
                    '\u200b',
                    '*no match*',
                ).add_thumbnail(
                    guild.icon_url,
                ),
            ),
        )
    finally:
        client._delete()
        client = None
