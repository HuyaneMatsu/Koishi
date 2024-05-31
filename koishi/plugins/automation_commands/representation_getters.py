__all__ = ()

from dateutil.relativedelta import relativedelta as RelativeDelta
from hata import CHANNELS, EMOJIS, ROLES, elapsed_time

from .constants import CHOICE_DEFAULT, ENTITY_REPRESENTATION_DEFAULT


def get_channel_id_representation(channel_id):
    """
    Gets channel mention for the given identifier.
    
    Parameters
    ----------
    channel_id : `int`
        The channel's identifier.
    
    Returns
    -------
    representation : `str`
    """
    if not channel_id:
        return ENTITY_REPRESENTATION_DEFAULT
        
    try:
        channel = CHANNELS[channel_id]
    except KeyError:
        return ENTITY_REPRESENTATION_DEFAULT
    
    return channel.mention


def get_emoji_representation(emoji):
    """
    Gets the emoji's representation.
    
    Parameters
    ----------
    emoji : `None | Emoji`
        The emoji.
    
    Returns
    -------
    representation : `str`
    """
    if emoji is None:
        return ENTITY_REPRESENTATION_DEFAULT
    
    return emoji.as_emoji


def get_emoji_id_representation(emoji_id):
    """
    Gets an emoji's representation for the given identifier.
    
    Parameters
    ----------
    emoji_id : `int`
        The emoji's identifier.
    
    Returns
    -------
    representation : `str`
    """
    if not emoji_id:
        return ENTITY_REPRESENTATION_DEFAULT
    
    try:
        emoji = EMOJIS[emoji_id]
    except KeyError:
        return f'<{emoji_id!s}>'
    
    return emoji.as_emoji


def get_role_id_representation(role_id):
    """
    Gets role mention for the given identifier.
    
    Parameters
    ----------
    role_id : `int`
        The role's identifier.
    
    Returns
    -------
    representation : `str`
    """
    if not role_id:
        return ENTITY_REPRESENTATION_DEFAULT
        
    try:
        role = ROLES[role_id]
    except KeyError:
        return ENTITY_REPRESENTATION_DEFAULT
    
    return role.mention


def get_bool_representation(value):
    """
    Gets the boolean's representation.
    
    Parameters
    ----------
    value : `bool`
        The value to get its representation of.
    
    Returns
    -------
    representation : `str`
    """
    return 'enabled' if value else 'disabled'


def get_choice_representation(value):
    """
    Returns the choice's representation.
    
    Parameters
    ----------
    value : `None | str`
        Choice value.
    
    Returns
    -------
    representation : `str`
    """
    if value is None:
        return CHOICE_DEFAULT
    
    return value


def get_duration_representation(duration):
    """
    Renders duration representation.
    
    Parameters
    ----------
    duration : `int`
        Duration in seconds.
    
    Returns
    -------
    representation : `str`
    """
    return elapsed_time(RelativeDelta(seconds = duration))
