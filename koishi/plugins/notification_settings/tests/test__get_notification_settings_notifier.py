import vampytest
from hata import Client, ClientWrapper, Guild, GuildProfile, InteractionEvent, User

from ..utils import get_notification_settings_notifier


def _assert_output_structure(output):
    """
    Asserts whether the output's structure is correct.
    
    Parameters
    ----------
    output : `(bool, None | Client)`
    """
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    hit, client = output
    vampytest.assert_instance(hit, bool)
    vampytest.assert_instance(client, Client, nullable = True)
    

def test__get_notification_settings_notifier__no_input():
    """
    Tests whether ``get_notification_settings_notifier`` works as intended.
    
    Case: no input.
    """
    user_id = 202402260001
    
    user = User.precreate(user_id)
    event = InteractionEvent(
        user = user,
    )
    
    output = get_notification_settings_notifier(event, '')
    
    _assert_output_structure(output)
    hit, client = output
    vampytest.assert_eq(hit, True)
    vampytest.assert_is(client, None)


def test__get_notification_settings_notifier__default():
    """
    Tests whether ``get_notification_settings_notifier`` works as intended.
    
    Case: matching default.
    """
    user_id = 202402260002
    
    user = User.precreate(user_id)
    event = InteractionEvent(
        user = user,
    )
    
    output = get_notification_settings_notifier(event, 'un')
    
    _assert_output_structure(output)
    hit, client = output
    vampytest.assert_eq(hit, True)
    vampytest.assert_is(client, None)


def test__get_notification_settings_notifier__client():
    """
    Tests whether ``get_notification_settings_notifier`` works as intended.
    
    Case: matching a client.
    """
    client_id_0 = 202402260003
    client_id_1 = 202402260004
    guild_id_0 = 202402260005
    guild_id_1 = 202402260006
    user_id = 202402260007
    client_name_0 = 'koishi'
    client_name_1 = 'satori'
    
    user = User.precreate(user_id)
    event = InteractionEvent(
        user = user,
    )
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
        name = client_name_0,
    )

    client_1 = Client(
        'token' + str(client_id_1),
        client_id = client_id_1,
        name = client_name_1,
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
    
    mocked = vampytest.mock_globals(get_notification_settings_notifier, 2, FEATURE_CLIENTS = FEATURE_CLIENTS)
    
    try:
        output = mocked(event, 'sato')
        
        _assert_output_structure(output)
        hit, client = output
        vampytest.assert_eq(hit, True)
        vampytest.assert_is(client, client_1)
    
    finally:
        FEATURE_CLIENTS = None
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None

    user_id = 202402260002
    
    user = User.precreate(user_id)
    event = InteractionEvent(
        user = user,
    )
    
    output = get_notification_settings_notifier(event, 'un')
    
    _assert_output_structure(output)
    hit, client = output
    vampytest.assert_eq(hit, True)
    vampytest.assert_is(client, None)


def test__get_notification_settings_notifier__no_match():
    """
    Tests whether ``get_notification_settings_notifier`` works as intended.
    
    Case: no match.
    """
    user_id = 202402260012
    
    user = User.precreate(user_id)
    event = InteractionEvent(
        user = user,
    )
    
    output = get_notification_settings_notifier(event, 'mister')
    
    _assert_output_structure(output)
    hit, client = output
    vampytest.assert_eq(hit, False)
    vampytest.assert_is(client, None)
