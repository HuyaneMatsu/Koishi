import vampytest
from hata import Client, ClientWrapper, Guild, GuildProfile, User

from ..utils import get_available_clients


def test__get_available_clients():
    """
    Tests whether ``get_available_clients`` works as intended.
    """
    client_id_0 = 202402250015
    client_id_1 = 202402250016
    guild_id_0 = 202402250017
    guild_id_1 = 202402250018
    user_id = 202402250019
    
    user = User.precreate(user_id)
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
    )

    client_1 = Client(
        'token' + str(client_id_1),
        client_id = client_id_1,
    )
    guild_0 = Guild.precreate(guild_id_0)
    guild_1 = Guild.precreate(guild_id_1)
    
    user.guild_profiles[guild_id_0] = GuildProfile()
    user.guild_profiles[guild_id_1] = GuildProfile()
    
    guild_0.clients.append(client_0)
    guild_1.clients.append(client_1)
    
    FEATURE_CLIENTS = ClientWrapper(
        client_0,
        client_1,
    )
    
    mocked = vampytest.mock_globals(get_available_clients, FEATURE_CLIENTS = FEATURE_CLIENTS)
    
    try:
        output = mocked(user)
        vampytest.assert_instance(output, set)
        vampytest.assert_eq(output, {client_0, client_1})
    
    finally:
        FEATURE_CLIENTS = None
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
