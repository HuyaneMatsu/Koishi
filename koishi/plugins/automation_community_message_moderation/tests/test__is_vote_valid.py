import vampytest
from hata import Channel, ChannelType, Guild, GuildProfile, Role, User

from ..helpers import PERMISSION_MASK_MESSAGING_DEFAULT, is_vote_valid


def test__is_vote_valid__bot():
    """
    Tests whether ``is_vote_valid`` works as intended.
    
    Case: The user is a bot.
    """
    guild = Guild.precreate(202401160005)
    channel = Channel.precreate(202401160003, guild_id = guild.id, channel_type = ChannelType.guild_text)
    user = User.precreate(202401160004, bot = True)
    user.guild_profiles[guild.id] = GuildProfile()
    guild.users[user.id] = user
    role = Role.precreate(
        guild.id,
        guild_id = guild.id,
        permissions = PERMISSION_MASK_MESSAGING_DEFAULT.update_by_keys(view_channel = True),
    )
    guild.roles[role.id] = role
    guild.channels[channel.id] = channel
    
    def is_user_id_in_blacklist_mock(user_id):
        nonlocal user
        vampytest.assert_eq(user_id, user.id)
        return False
    
    mocked = vampytest.mock_globals(
        is_vote_valid,
        is_user_id_in_blacklist = is_user_id_in_blacklist_mock,
    )
    
    output = mocked(channel, user, PERMISSION_MASK_MESSAGING_DEFAULT)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__is_vote_valid__missing_permissions():
    """
    Tests whether ``is_vote_valid`` works as intended.
    
    Case: The user has missing permissions
    """
    guild = Guild.precreate(202401160006)
    channel = Channel.precreate(202401160007, guild_id = guild.id, channel_type = ChannelType.guild_text)
    user = User.precreate(202401160008, bot = False)
    user.guild_profiles[guild.id] = GuildProfile()
    guild.users[user.id] = user
    role = Role.precreate(
        guild.id,
        guild_id = guild.id,
        permissions = 0,
    )
    guild.roles[role.id] = role
    guild.channels[channel.id] = channel
    
    def is_user_id_in_blacklist_mock(user_id):
        nonlocal user
        vampytest.assert_eq(user_id, user.id)
        return False
    
    mocked = vampytest.mock_globals(
        is_vote_valid,
        is_user_id_in_blacklist = is_user_id_in_blacklist_mock,
    )
    
    output = mocked(channel, user, PERMISSION_MASK_MESSAGING_DEFAULT)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__is_vote_valid__blacklisted():
    """
    Tests whether ``is_vote_valid`` works as intended.
    
    Case: The user has missing permissions
    """
    guild = Guild.precreate(202401160009)
    channel = Channel.precreate(202401160010, guild_id = guild.id, channel_type = ChannelType.guild_text)
    user = User.precreate(202401160011, bot = False)
    user.guild_profiles[guild.id] = GuildProfile()
    guild.users[user.id] = user
    role = Role.precreate(
        guild.id,
        guild_id = guild.id,
        permissions = PERMISSION_MASK_MESSAGING_DEFAULT.update_by_keys(view_channel = True),
    )
    guild.roles[role.id] = role
    guild.channels[channel.id] = channel
    
    def is_user_id_in_blacklist_mock(user_id):
        nonlocal user
        vampytest.assert_eq(user_id, user.id)
        return True
    
    mocked = vampytest.mock_globals(
        is_vote_valid,
        is_user_id_in_blacklist = is_user_id_in_blacklist_mock,
    )
    
    output = mocked(channel, user, PERMISSION_MASK_MESSAGING_DEFAULT)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, False)


def test__is_vote_valid_passing():
    """
    Tests whether ``is_vote_valid`` works as intended.
    
    Case: The user has missing permissions
    """
    guild = Guild.precreate(202401160012)
    channel = Channel.precreate(202401160013, guild_id = guild.id, channel_type = ChannelType.guild_text)
    user = User.precreate(202401160014, bot = False)
    user.guild_profiles[guild.id] = GuildProfile()
    guild.users[user.id] = user
    role = Role.precreate(
        guild.id,
        guild_id = guild.id,
        permissions = PERMISSION_MASK_MESSAGING_DEFAULT.update_by_keys(view_channel = True),
    )
    guild.roles[role.id] = role
    guild.channels[channel.id] = channel
    
    def is_user_id_in_blacklist_mock(user_id):
        nonlocal user
        vampytest.assert_eq(user_id, user.id)
        return False
    
    mocked = vampytest.mock_globals(
        is_vote_valid,
        is_user_id_in_blacklist = is_user_id_in_blacklist_mock,
    )
    
    output = mocked(channel, user, PERMISSION_MASK_MESSAGING_DEFAULT)
    vampytest.assert_instance(output, bool)
    vampytest.assert_eq(output, True)
