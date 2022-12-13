__all__ = ()

from .constants import (
    ICON_KIND_AVATAR, ICON_KIND_BANNER, ICON_SOURCE_DEFAULT, ICON_SOURCE_GLOBAL, ICON_SOURCE_GUILD, ICON_SOURCE_LOCAL
)


def get_avatar_of(user, guild_id, icon_source):
    """
    Gets the avatar url of the user in the given context.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    icon_url : `None`, `str`
    """
    if icon_source == ICON_SOURCE_LOCAL:
        icon_url = user.avatar_url_at_as(guild_id, size = 4096)
    
    elif icon_source == ICON_SOURCE_GLOBAL:
        icon_url = user.avatar_url_as(size = 4096)
    
    elif icon_source == ICON_SOURCE_GUILD:
        icon_url = user.avatar_url_for_as(guild_id, size = 4096)
    
    elif icon_source == ICON_SOURCE_DEFAULT:
        icon_url = user.default_avatar_url
        
    else:
        icon_url = None
    
    return icon_url


def get_banner_of(user, guild_id, icon_source):
    """
    Gets the banner url of the user in the given context.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    icon_url : `None`, `str`
    """
    if icon_source == ICON_SOURCE_GLOBAL:
        icon_url = user.banner_url_as(size = 4096)
    
    else:
        icon_url = None
        
    return icon_url


def get_icon_of(user, guild_id, icon_kind, icon_source):
    """
    Gets the defined icon url of the user in the given context.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    guild_id : `int`
        The context's guild's identifier.
    icon_kind : `int`
        Which icon should be taken of the user.
    icon_source : `int`
        From which source should be the icon taken from.
    
    Returns
    -------
    icon_url : `None`, `str`
    """
    if icon_kind == ICON_KIND_AVATAR:
        return get_avatar_of(user, guild_id, icon_source)
    
    if icon_kind == ICON_KIND_BANNER:
        return get_banner_of(user, guild_id, icon_source)
    
    return None
