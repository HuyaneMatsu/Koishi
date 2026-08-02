import vampytest
from hata import Client, Guild, GuildProfile, User

from ..helpers import iter_select_client_with_shared_guild


def test__iter_select_client_with_shared_guild():
    """
    Tests whether ``iter_select_client_with_shared_guild`` works as intended.
    """
    client_id_0 = 202607310000
    client_id_1 = 202607310001
    
    user_id_0 = 202607310002
    
    guild_id_0 = 202607310003
    guild_id_1 = 202607310004
    
    clients = []
    
    try:
        try:
            client_0 = Client(f'token_{client_id_0}', client_id = client_id_0)
            client_0.guild_profiles[guild_id_1] = GuildProfile()
            clients.append(client_0)
        finally:
            client_0 = None
        
        try:
            client_1 = Client(f'token_{client_id_1}', client_id = client_id_1)
            client_1.guild_profiles[guild_id_1] = GuildProfile()
            client_1.guild_profiles[guild_id_0] = GuildProfile()
            clients.append(client_1)
        finally:
            client_1 = None
        
        user_0 = User.precreate(user_id_0)
        user_0.guild_profiles[guild_id_0] = GuildProfile()
        user_0.guild_profiles[guild_id_1] = GuildProfile()
        
        guild_0 = Guild.precreate(guild_id_0, users = [user_0, clients[1]])
        guild_0.clients.append(clients[1])
        
        guild_1 = Guild.precreate(guild_id_1, users = [user_0, clients[1], clients[0]])
        guild_1.clients.append(clients[1])
        guild_1.clients.append(clients[0])
        
        output = [*iter_select_client_with_shared_guild(user_0)]
        try:
            for element in output:
                vampytest.assert_instance(element, Client)
        finally:
            element = None
        
        vampytest.assert_eq(
            {element.id for element in output},
            {client_id_0, client_id_1},
        )
        
    finally:
        try:
            for client in clients:
                client._delete()
        finally:
            client = None
            clients = None
        
        output = None
