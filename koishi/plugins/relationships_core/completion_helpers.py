__all__ = ('looks_like_user_id',)


def looks_like_user_id(value):
    """
    Returns whether the given value looks like a user identifier.
    
    Parameters
    ----------
    value : `None | str`
        Value to match.
    
    Returns
    -------
    looks_like_user_id : `bool`
    """
    return value.isdigit() and (17 <= len(value) <= 21)
    

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
    suggestions `None | list<(str, str)>`
    """
    while True:
        if value is None:
            suggestions = [
                (user.name_at(guild_id), str(user.id))
                for user in users
            ]
            break
        
        if looks_like_user_id(value):
            passed_user_id = int(value)
            
            for user in users:
                if user.id == passed_user_id:
                    break
            else:
                user = None
            
            if (user is not None):
                suggestions = [
                    (user.name_at(guild_id), str(user.id))
                ]
                break
        
        suggestions = [
            (user.name_at(guild_id), str(user.id))
            for user in users
            if user.has_name_like_at(value, guild_id)
        ]
        break
    
    if suggestions:
        suggestions.sort()
    else:
        suggestions = None
    
    return suggestions
