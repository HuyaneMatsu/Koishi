__all__ = ()

def _make_suggestions(users, value, guild_id):
    """
    Make suggestions for the given users.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The users to make suggestions for.
    
    value : `None | str`
        Value to get suggestions for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    suggestions `None | list<str>`
    """
    while True:
        if value is None:
            suggestions = [user.name_at(guild_id) for user in users]
        else:
            suggestions = [user.name_at(guild_id) for user in users if user.has_name_like_at(value, guild_id)]
            if not suggestions:
                suggestions = None
                break
        
        suggestions.sort()
        break
    
    return suggestions
