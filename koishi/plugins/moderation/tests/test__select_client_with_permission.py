import vampytest
from hata import Client, Guild, GuildProfile, Role

from ..helpers import select_client_with_permission


def _iter_options():
    yield (
        202607150030,
        202607150031,
        (
            (
                202607150030,
                'Suwako',
                False,
                0,
                0,
                0,
            ),
        ),
        0b101,
        0,
    )
    
    yield (
        202607150040,
        202607150041,
        (
            (
                202607150040,
                'Suwako',
                True,
                202607150042,
                1,
                0,
            ),
        ),
        0b101,
        0,
    )
    
    yield (
        202607150050,
        202607150051,
        (
            (
                202607150050,
                'Suwako',
                True,
                202607150052,
                1,
                0b101,
            ),
        ),
        0b101,
        202607150050,
    )
    
    yield (
        202607150060,
        202607150061,
        (
            (
                202607150063,
                'Suwako',
                True,
                202607150062,
                1,
                0b101,
            ),
            (
                202607150060,
                'Suwako',
                True,
                202607150062,
                1,
                0b101,
            ),
        ),
        0b101,
        202607150060,
    )
    
    yield (
        202607150070,
        202607150071,
        (
            (
                202607150070,
                'Suwako',
                True,
                202607150072,
                1,
                0b101,
            ),
            (
                202607150073,
                'Kanako',
                True,
                202607150074,
                2,
                0b101,
            ),
        ),
        0b101,
        202607150073,
    )
    
    yield (
        202607150080,
        202607150081,
        (
            (
                202607150080,
                'Suwako',
                True,
                202607150082,
                1,
                0b101,
            ),
            (
                202607150083,
                'Suwako',
                True,
                202607150084,
                0,
                0b101,
            ),
        ),
        0b101,
        202607150080,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_client_with_permission(
    client_id,
    guild_id,
    client_id_and_name_include_in_guild_and_role_id_and_position_and_permissions,
    required_permission,
):
    """
    Tests whether ``select_client_with_permission`` works as intended.
    
    Parameters
    ----------
    client_id : `int`
        The user's identifier.
    
    guild_id : `int`
        Gild identifier to create guild with.
    
    interaction_event_id : `int`
        Interaction event identifier to create interaction event with.
    
    client_id_and_name_include_in_guild_and_role_id_and_position_and_permissions : `tuple<(int, str, bool, int, int, int)>`
        Client identifiers, whether to put them into the guild and their permissions.
    
    required_permission : ``Permission``
        The required permissions to execute the action.
   
    Returns
    -------
    output : ``int``
    """
    clients = []
    roles = []
    users = []
    
    try:
        role = Role.precreate(guild_id)
        roles.append(role)
        
        for (
            client_id_iterated, client_name, include_in_guild, role_id, position, permissions
        ) in client_id_and_name_include_in_guild_and_role_id_and_position_and_permissions:
            client = Client(
                f'token_{client_id}',
                client_id = client_id_iterated,
                name = client_name,
            )
            clients.append(client)
            
            if include_in_guild:
                if role_id:
                    role = Role.precreate(role_id, position = position, permissions = permissions)
                    roles.append(role)
                
                client.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id] if role_id else None)
                users.append(client)
        
        guild = Guild.precreate(
            guild_id,
            roles = roles,
            users = users,
        )
        guild.clients.extend(users)
        
        for client in clients:
            if client.id == client_id:
                break
        else:
            assert False
        
        selected_client = select_client_with_permission(client, guild, required_permission)
        vampytest.assert_instance(selected_client, Client, nullable = True)
        selected_client_id = 0 if selected_client is None else selected_client.id
    finally:
        while clients:
            clients.pop()._delete()
        
        client = None
    
    return selected_client_id
