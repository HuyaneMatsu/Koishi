import vampytest
from hata import Channel, ChannelType, Guild, GuildProfile, User

from ..helpers import is_private_channel_of_two


def _iter_options():
    user_id_0 = 202502080000
    user_id_1 = 202502080001
    user_id_2 = 202502080002
    guild_id = 202502080003
    channel_id_0 = 202502080004
    channel_id_1 = 202502080007
    channel_id_2 = 202502080008
    channel_id_3 = 202502080009
    channel_id_4 = 202502080020
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    user_0.guild_profiles[guild_id] = GuildProfile()
    user_1.guild_profiles[guild_id] = GuildProfile()
    
    guild = Guild.precreate(guild_id, users = [user_0, user_1])
    
    yield (
        Channel.precreate(channel_id_0, channel_type = ChannelType.guild_text, guild_id = guild_id),
        user_0,
        user_1,
        [guild],
        False,
    )
    
    yield (
        Channel.precreate(channel_id_1, channel_type = ChannelType.private, users = [user_0, user_2]),
        user_0,
        user_1,
        None,
        False,
    )
    
    yield (
        Channel.precreate(channel_id_2, channel_type = ChannelType.private, users = [user_0, user_1]),
        user_0,
        user_1,
        None,
        True,
    )
    
    yield (
        Channel.precreate(channel_id_3, channel_type = ChannelType.private_group, users = [user_0, user_2]),
        user_0,
        user_1,
        None,
        False,
    )
    
    yield (
        Channel.precreate(channel_id_4, channel_type = ChannelType.private_group, users = [user_0, user_1]),
        user_0,
        user_1,
        None,
        True,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_private_channel_of_two(channel, source_user, target_user, cache):
    """
    Tests whether ``is_private_channel_of_two`` works as intended.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to check.
    
    source_user : ``ClientUserBase``
        The user to be in the channel.
    
    target_user : ``ClientUserBase``
        The other user to be in the channel.
    
    cache : `None | list<object>`
        Additional objects to keep in the cache.
    
    Returns
    -------
    output : `bool`
    """
    output = is_private_channel_of_two(channel, source_user, target_user)
    vampytest.assert_instance(output, bool)
    return output
