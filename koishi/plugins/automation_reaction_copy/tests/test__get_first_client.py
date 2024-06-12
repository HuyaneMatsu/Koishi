import vampytest

from hata import (
    Channel, ChannelType, Client, Guild, GuildProfile, PermissionOverwrite, PermissionOverwriteTargetType, Role
)

from ..list_channels import get_first_client


def test__get_first_client():
    """
    Tests whether ``get_first_client`` works as intended.
    """
    client_id_0 = 202406120000
    client_id_1 = 202406120001
    client_id_2 = 202406120002
    channel_id = 202406120003
    guild_id = 202406120004
    
    client_0 = Client(
        'token ' + str(client_id_0),
        client_id = client_id_0,
    )
    client_0.guild_profiles[guild_id] = GuildProfile()
    
    client_1 = Client(
        'token ' + str(client_id_1),
        client_id = client_id_1,
    )
    client_1.guild_profiles[guild_id] = GuildProfile()
    
    client_2 = Client(
        'token ' + str(client_id_2),
        client_id = client_id_2,
    )
    client_2.guild_profiles[guild_id] = GuildProfile()
    
    channel = Channel.precreate(
        channel_id,
        channel_type = ChannelType.guild_text,
        guild_id = guild_id,
        permission_overwrites = [
            PermissionOverwrite(client_id_1, target_type = PermissionOverwriteTargetType.user, allow = 8),
            PermissionOverwrite(client_id_2, target_type = PermissionOverwriteTargetType.user, allow = 8),
        ],
    )
    
    role = Role.precreate(
        guild_id,
        permissions = 0
    )
    
    guild = Guild.precreate(
        guild_id,
        channels = [channel],
        roles = [role],
        users = [client_0, client_1, client_2],
    )
    guild.clients.append(client_0)
    guild.clients.append(client_1)
    guild.clients.append(client_2)
    
    try:
        output = get_first_client(channel)
        vampytest.assert_is(output, client_1)
    
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
        client_2._delete()
        client_2 = None
