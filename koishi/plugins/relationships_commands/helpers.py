__all__ = ()

from hata import ChannelType


def is_private_channel_of_two(channel, source_user, target_user):
    """
    Returns whether the given private channel is teh private channel of the two users.
    
    Parameters
    ----------
    channel : ``Channel``
        The channel to check.
    
    source_user : ``ClientUserBase``
        The user to be in the channel.
    
    target_user : ``ClientUserBase``
        The other user to be in the channel.
    
    Returns
    -------
    private_channel_of_two : `bool`
    """
    channel_type = channel.type
    if (channel_type is not ChannelType.private) and (channel_type is not ChannelType.private_group):
        return False
    
    users = channel.users
    if (source_user not in users) or (target_user not in users):
        return False
    
    return True
