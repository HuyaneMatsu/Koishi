import vampytest

from hata import (
    Client, BUILTIN_EMOJIS, Channel, ChannelType, Emoji, Guild, GuildProfile,
    PermissionOverwrite, PermissionOverwriteTargetType, escape_markdown
)

from ..list_channels import build_description


def test__build_description():
    """
    Tests whether ``build_description`` works as intended.
    """
    channel_id_0 = 202406090013
    channel_id_1 = 202406090014
    channel_id_2 = 202406090015
    emoji_id_0 = 202406100000
    guild_id = 202406120005
    client_id = 202406120006
    
    channel_0 = Channel.precreate(
        channel_id_0,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        position = 10,
        permission_overwrites = [
            PermissionOverwrite(client_id, target_type = PermissionOverwriteTargetType.user, allow = 8),
        ],
    )
    
    channel_1 = Channel.precreate(
        channel_id_1,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        position = 9,
    )
    
    channel_2 = Channel.precreate(
        channel_id_2,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        position = 8,
        permission_overwrites = [
            PermissionOverwrite(client_id, target_type = PermissionOverwriteTargetType.user, allow = 8),
        ],
    )
    
    emoji_0 = BUILTIN_EMOJIS['heart']
    emoji_1 = BUILTIN_EMOJIS['blue_heart']
    emoji_2 = BUILTIN_EMOJIS['black_heart']
    emoji_3 = BUILTIN_EMOJIS['green_heart']
    emoji_4 = Emoji.precreate(emoji_id_0, name = 'pudding')
    
    channels_and_emojis = [
        (channel_2, [emoji_2, emoji_3]),
        (channel_1, [emoji_4]),
        (channel_0, [emoji_0, emoji_1]),
    ]
    
    client = Client(
        'token_' + str(client_id),
        client_id = client_id,
    )
    client.guild_profiles[guild_id] = GuildProfile()

    guild = Guild.precreate(
        guild_id,
        channels = [channel_0, channel_1, channel_2],
        users = [client],
    )
    guild.clients.append(client)
    
    try:
        output = build_description(channels_and_emojis)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_eq(
            output,
            (
                f'{channel_2.mention} : {emoji_2} \\:black\\_heart\\: | {emoji_3} \\:green\\_heart\\:\n'
                f'{channel_1.mention} : {emoji_4} {escape_markdown(emoji_4.as_emoji)!s} (missing permissions)\n'
                f'{channel_0.mention} : {emoji_0} \\:heart\\: | {emoji_1} \\:blue\\_heart\\:'
            ),
        )
    finally:
        client._delete()
        client = None
