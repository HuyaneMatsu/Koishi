import vampytest
from hata import Client, Guild, GuildProfile, Permission, Role

from ..helpers import get_highest_client_with_role


def test__get_highest_client_with_role__no_guild():
    """
    Tests whether ``get_highest_client_with_role`` works as intended.
    
    Case: no guild.
    """
    guild = None
    
    output = get_highest_client_with_role(guild)
    
    vampytest.assert_instance(output, tuple, nullable = True)
    vampytest.assert_is(output, None)


def test__get_highest_client_with_role__no_client_hit():
    """
    Tests whether ``get_highest_client_with_role`` works as intended.
    
    Case: no client hit.
    """
    client_id_0 = 202510020030
    client_id_1 = 202510020033
    guild_id = 202510020031
    role_id_0 = 202510020032
    
    client_0 = Client(
        f'token {client_id_0}',
        client_id = client_id_0,
    )
    
    try:
        client_1 = Client(
            f'token {client_id_1}',
            client_id = client_id_1,
        )
        
        try:
            role_0 = Role.precreate(
                role_id_0,
                guild_id = guild_id,
                position = 4,
            )
            
            role_default = Role.precreate(
                guild_id,
                guild_id = guild_id,
            )
            
            guild = Guild.precreate(
                guild_id,
                roles = [role_0, role_default]
            )
            guild.clients.append(client_0)
            guild.clients.append(client_1)
            client_0.guild_profiles[guild_id] = GuildProfile(role_ids = [])
            client_1.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
        
            output = get_highest_client_with_role(guild)
            
            vampytest.assert_instance(output, tuple, nullable = True)
            vampytest.assert_is(output, None)
    
        finally:
            client_1._delete()
            client_1 = None
    
    finally:
        client_0._delete()
        client_0 = None


def test__get_highest_client_with_role__client_hit():
    """
    Tests whether ``get_highest_client_with_role`` works as intended.
    
    Case: client hit.
    """
    client_id_0 = 202510020040
    client_id_1 = 202510020043
    guild_id = 202510020041
    role_id_0 = 202510020042
    
    client_0 = Client(
        f'token {client_id_0}',
        client_id = client_id_0,
    )
    
    try:
        client_1 = Client(
            f'token {client_id_1}',
            client_id = client_id_1,
        )
        
        try:
            role_0 = Role.precreate(
                role_id_0,
                guild_id = guild_id,
                position = 4,
            )
            
            role_default = Role.precreate(
                guild_id,
                guild_id = guild_id,
                permissions = Permission().update_by_keys(manage_roles = True),
            )
            
            guild = Guild.precreate(
                guild_id,
                roles = [role_0, role_default]
            )
            guild.clients.append(client_0)
            guild.clients.append(client_1)
            client_0.guild_profiles[guild_id] = GuildProfile(role_ids = [])
            client_1.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id_0])
        
            output = get_highest_client_with_role(guild)
            
            vampytest.assert_instance(output, tuple, nullable = True)
            vampytest.assert_eq(output, (client_1, role_0))
    
        finally:
            client_1._delete()
            client_1 = None
    
    finally:
        client_0._delete()
        client_0 = None
