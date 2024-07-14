import vampytest
from hata import Channel, ChannelType, Client, Guild, GuildProfile, InteractionEvent, Permission, Role, User

from ...user_settings import UserSettings

from ..commands import get_should_use_default_response_method


async def test__get_should_use_default_response_method__permissions():
    """
    Tests whether ``get_should_use_default_response_method`` works as intended.
    
    Case: Permissions.
    
    This function is a coroutine.
    """
    client_id_0 = 202407130000
    interaction_event_id = 202407130001
    guild_id = 202407130002
    channel_id = 202407130003
    user_id = 202407130004
    
    client_0 = Client(
        'token_' + str(client_id_0),
        client_id = client_id_0,
    )
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    guild = Guild.precreate(guild_id, channels = [channel])
    user = User.precreate(user_id)
    
    event = InteractionEvent.precreate(
        interaction_event_id,
        channel = channel,
        guild = guild,
        user_permissions = Permission().update_by_keys(use_external_application_commands = True),
        user = user,
    )
    
    user_settings = UserSettings(user_id)
    
    async def get_one_user_settings_mock(user_id):
        nonlocal user_settings
        return user_settings
        
    
    mocked = vampytest.mock_globals(
        get_should_use_default_response_method,
        get_one_user_settings = get_one_user_settings_mock,
    )
    
    try:
        output = await mocked(client_0, event)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        
        vampytest.assert_eq(output[0], True)
        vampytest.assert_is(output[1], client_0)
    finally:
        client_0._delete()
        client_0 = None


async def test__get_should_use_default_response_method__no_permissions_different_client():
    """
    Tests whether ``get_should_use_default_response_method`` works as intended.
    
    Case: No permissions & different client..
    
    This function is a coroutine.
    """
    client_id_0 = 202407130005
    client_id_1 = 202407130010
    interaction_event_id = 202407130006
    guild_id = 202407130007
    channel_id = 202407130008
    user_id = 202407130009
    
    client_0 = Client(
        'token_' + str(client_id_0),
        client_id = client_id_0,
    )
    
    client_1 = Client(
        'token_' + str(client_id_1),
        client_id = client_id_1,
    )
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, permissions = Permission(8), guild_id = guild_id)
    guild = Guild.precreate(guild_id, channels = [channel], roles = [role])
    user = User.precreate(user_id)
    
    guild.clients = [client_0, client_1]
    client_0.guild_profiles[guild_id] = GuildProfile()
    client_1.guild_profiles[guild_id] = GuildProfile()
    
    
    event = InteractionEvent.precreate(
        interaction_event_id,
        channel = channel,
        guild = guild,
        user_permissions = Permission().update_by_keys(use_external_application_commands = False),
        user = user,
    )
    
    user_settings = UserSettings(user_id, preferred_client_id = client_id_1)
    
    async def get_one_user_settings_mock(user_id):
        nonlocal user_settings
        return user_settings
        
    
    mocked = vampytest.mock_globals(
        get_should_use_default_response_method,
        get_one_user_settings = get_one_user_settings_mock,
    )
    
    try:
        output = await mocked(client_0, event)
        
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        
        vampytest.assert_eq(output[0], False)
        vampytest.assert_is(output[1], client_1)
    finally:
        client_0._delete()
        client_0 = None
        client_1._delete()
        client_1 = None
