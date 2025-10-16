__all__ = ()

from hata import EMOJIS, ROLES


def get_emoji_name(user, emoji_id):
    """
    Gets the emoji's name.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The use from who's view point we are inspecting the emoji.
    
    emoji_id : `int`
        The emoji's identifier.
    """
    try:
        emoji = EMOJIS[emoji_id]
    except KeyError:
        return 'unknown'
    
    if user.can_use_emoji(emoji):
        return f'{emoji} {emoji.name}'
    
    return emoji.name


def produce_role_listing(role_ids):
    """
    Produces a single role listing.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    role_ids : `tuple<int>`
        Role identifiers.
    
    Yields
    ------
    part : `str`
    """
    for role_id in role_ids:
        yield '\n- '
        
        try:
            role = ROLES[role_id]
        except KeyError:
            yield '@\u200bdeleted role'
        else:
            yield role.mention
