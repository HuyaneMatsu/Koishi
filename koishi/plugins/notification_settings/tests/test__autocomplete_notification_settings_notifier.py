import vampytest
from hata import Client, ClientWrapper, Guild, GuildProfile, InteractionEvent, User

from ..constants import NOTIFIER_NAME_DEFAULT
from ..utils import autocomplete_notification_settings_notifier


async def test__autocomplete_notification_settings_notifier__none():
    """
    Tests whether ``autocomplete_notification_settings_notifier`` works as intended.
    
    Case: No value.
    """
    client_id_0 = 202402250031
    client_id_1 = 202402250032
    guild_id_0 = 202402250033
    guild_id_1 = 202402250034
    user_id = 202402250035
    
    client_0_name = 'satori'
    client_1_name = 'koishi'
    
    user = User.precreate(user_id)
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
        name = client_0_name,
    )

    client_1 = Client(
        'token' + str(client_id_1),
        client_id = client_id_1,
        name = client_1_name,
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
    
    event = InteractionEvent(
        user = user,
    )
    
    mocked = vampytest.mock_globals(autocomplete_notification_settings_notifier, 2, FEATURE_CLIENTS = FEATURE_CLIENTS)
    
    try:
        output = await mocked(event, None)
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(output, [NOTIFIER_NAME_DEFAULT, client_1_name, client_0_name])
    
    finally:
        FEATURE_CLIENTS = None
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


async def test__autocomplete_notification_settings_notifier__value_excluding_default():
    """
    Tests whether ``autocomplete_notification_settings_notifier`` works as intended.
    
    Case: With value excluding default.
    """
    client_id_0 = 202402250036
    client_id_1 = 202402250037
    guild_id_0 = 202402250038
    guild_id_1 = 202402250039
    user_id = 202402250040
    
    client_0_name = 'satori'
    client_1_name = 'koishi'
    
    user = User.precreate(user_id)
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
        name = client_0_name,
    )

    client_1 = Client(
        'token' + str(client_id_1),
        client_id = client_id_1,
        name = client_1_name,
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
    
    event = InteractionEvent(
        user = user,
    )
    
    mocked = vampytest.mock_globals(autocomplete_notification_settings_notifier, 2, FEATURE_CLIENTS = FEATURE_CLIENTS)
    
    try:
        output = await mocked(event, 'sato')
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(output, [client_0_name])
    
    finally:
        FEATURE_CLIENTS = None
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None


async def test__autocomplete_notification_settings_notifier__value_including_default():
    """
    Tests whether ``autocomplete_notification_settings_notifier`` works as intended.
    
    Case: With value including default.
    
    This function is a coroutine.
    """
    client_id_0 = 202402250041
    client_id_1 = 202402250042
    guild_id_0 = 202402250043
    guild_id_1 = 202402250044
    user_id = 202402250045
    
    client_0_name = 'satori'
    client_1_name = 'koishi'
    
    user = User.precreate(user_id)
    
    client_0 = Client(
        'token' + str(client_id_0),
        client_id = client_id_0,
        name = client_0_name,
    )

    client_1 = Client(
        'token' + str(client_id_1),
        client_id = client_id_1,
        name = client_1_name,
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
    
    event = InteractionEvent(
        user = user,
    )
    
    mocked = vampytest.mock_globals(autocomplete_notification_settings_notifier, 2, FEATURE_CLIENTS = FEATURE_CLIENTS)
    
    try:
        output = await mocked(event, 'set')
        vampytest.assert_instance(output, list)
        vampytest.assert_eq(output, [NOTIFIER_NAME_DEFAULT])
    
    finally:
        FEATURE_CLIENTS = None
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
