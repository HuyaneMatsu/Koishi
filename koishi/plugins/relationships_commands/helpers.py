__all__ = ()

from hata import ChannelType


def is_private_channel_of_two(channel, source_user, target_user):
    """
    Returns whether the given private channel is the private channel of the two users.
    
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


def select_existing_relationship(relationship_listing, source_user_id, target_user_id):
    """
    Selects the existing relationship between the two users.
    
    Parameters
    ----------
    relationship_listing : `None | list<Relationship>`
        The relationship listing of one of the users.
    
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The targeted user's identifier.
    
    Returns
    -------
    relationship : ``None | Relationship``
    """
    if (relationship_listing is None):
        return
    
    for relationship in relationship_listing:
        if (
            ((relationship.source_user_id == source_user_id) and (relationship.target_user_id == target_user_id)) or
            ((relationship.target_user_id == source_user_id) and (relationship.source_user_id == target_user_id))
        ):
            return relationship
