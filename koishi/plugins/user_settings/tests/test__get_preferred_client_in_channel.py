import vampytest

from hata import Channel, ChannelType, Client, Guild, GuildProfile, Permission, Role

from ..utils import get_preferred_client_in_channel


def test__get_preferred_client_in_channel__hit():
    """
    Tests whether ``get_preferred_client_in_channel`` works as intended.
    
    Case: Simple hit.
    """
    client_id_0 = 202404280003
    client_id_1 = 202404280004
    channel_id = 202404280005
    guild_id = 202404280006
    
    client_0 = Client(str(client_id_0) + '_token', client_id = client_id_0)
    client_1 = Client(str(client_id_1) + '_token', client_id = client_id_1)
    client_0.guild_profiles[guild_id] = GuildProfile()
    client_1.guild_profiles[guild_id] = GuildProfile()
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, guild_id = guild_id, permissions = Permission(8))
    guild = Guild.precreate(guild_id, channels = [channel], roles = [role], users = [client_0, client_1])
    
    
    try:
        output = get_preferred_client_in_channel(channel, client_id_0, client_1, 0)
        vampytest.assert_is(output, client_0)
    finally:
        client_0._delete()
        client_0 = None
        
        client_1._delete()
        client_1 = None


def test__get_preferred_client_in_channel__miss():
    """
    Tests whether ``get_preferred_client_in_channel`` works as intended.
    
    Case: Simple miss.
    """
    client_id_0 = 202404280007
    client_id_1 = 202404280008
    channel_id = 202404280009
    guild_id = 2024042800010
    
    client_0 = Client(str(client_id_0) + '_token', client_id = client_id_0)
    client_1 = Client(str(client_id_1) + '_token', client_id = client_id_1)
    # client_0.guild_profiles[guild_id] = GuildProfile()
    client_1.guild_profiles[guild_id] = GuildProfile()
    
    channel = Channel.precreate(channel_id, channel_type = ChannelType.guild_text, guild_id = guild_id)
    role = Role.precreate(guild_id, guild_id = guild_id, permissions = Permission(8))
    guild = Guild.precreate(guild_id, channels = [channel], roles = [role], users = [client_0, client_1])
    
    
    try:
        output = get_preferred_client_in_channel(channel, client_id_0, client_1, 0)
        vampytest.assert_is(output, client_1)
    finally:
        client_0._delete()
        client_0 = None
        
        client_1._delete()
        client_1 = None


def test__get_preferred_client_in_channel__no_preference():
    """
    Tests whether ``get_preferred_client_in_channel`` works as intended.
    
    Case: No preference.
    """
    client_id_0 = 202404280011
    channel_id_0 = 202404280012
    
    client_0 = Client(str(client_id_0) + '_token', client_id = client_id_0)
    channel = Channel.precreate(channel_id_0, channel_type = ChannelType.guild_text)
    
    try:
        output = get_preferred_client_in_channel(channel, 0, client_0, 0)
        vampytest.assert_is(output, client_0)
    finally:
        client_0._delete()
        client_0 = None
