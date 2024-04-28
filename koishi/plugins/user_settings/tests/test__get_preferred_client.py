import vampytest
from hata import Client, ClientWrapper, Guild, GuildProfile, User

from ..user_settings import UserSettings
from ..utils import get_preferred_client_for_user


def test__get_preferred_client_for_user__notifier_client_set():
    """
    Tests whether ``get_preferred_client_for_user`` works as intended.
    
    Case: notifier client set.
    """
    client_id_0 = 202402250020
    user_id = 202402250021
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
    )
    
    user = User.precreate(user_id)
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = client_id_0,
    )
    
    try:
        output = get_preferred_client_for_user(user, user_settings.preferred_client_id, None)
        
        vampytest.assert_instance(output, Client)
        vampytest.assert_eq(output, client_0)
    finally:
        client_0._delete()
        client_0 = None


def test__get_preferred_client_for_user__default_client_given():
    """
    Tests whether ``get_preferred_client_for_user`` works as intended.
    
    Case: notifier client set.
    """
    client_id_0 = 202402250022
    user_id = 202402250023
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
    )
    
    user = User.precreate(user_id)
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = 0,
    )
    
    try:
        output = get_preferred_client_for_user(user, user_settings.preferred_client_id, client_0)
        
        vampytest.assert_instance(output, Client)
        vampytest.assert_eq(output, client_0)
    finally:
        client_0._delete()
        client_0 = None


def test__get_preferred_client_for_user__available_clients():
    """
    Tests whether ``get_preferred_client_for_user`` works as intended.
    
    Case: user has available clients.
    """
    client_id_0 = 202402250024
    client_id_1 = 202402250025
    guild_id_0 = 202402250026
    guild_id_1 = 202402250027
    user_id = 202402250028
    
    user = User.precreate(user_id)
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = 0,
    )
    
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

    mocked = vampytest.mock_globals(get_preferred_client_for_user, 2, FEATURE_CLIENTS = FEATURE_CLIENTS)
    
    try:
        output = mocked(user, user_settings, None)
        
        vampytest.assert_instance(output, Client)
        vampytest.assert_in(output, {client_0, client_1})
    
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


def test__get_preferred_client_for_user__main_client():
    """
    Tests whether ``get_preferred_client_for_user`` works as intended.
    
    Case: defaulting to the main client.
    """
    client_id_0 = 202402250029
    user_id = 202402250030
    
    user = User.precreate(user_id)
    
    user_settings = UserSettings(
        user_id,
        preferred_client_id = 0,
    )
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
    )

    mocked = vampytest.mock_globals(get_preferred_client_for_user, MAIN_CLIENT = client_0)
    
    try:
        output = mocked(user, user_settings, None)
        
        vampytest.assert_instance(output, Client)
        vampytest.assert_is(output, client_0)
    
    finally:
        client_0._delete()
        client_0 = None
