__all__ = ()


from ...bot_utils.user_getter import get_user


async def get_relationship_request_entry_extra(user_id, session_id, amount, session):
    """
    Gets extra info for relationship request entry.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    session : ``None | RelationshipRequest``
        The game's session.
    
    Returns
    -------
    extra : ``None | (ClientUserBase, )``
    
    """
    if session is None:
        return None
    
    target_user = await get_user(session.target_user_id)
    return (target_user, )
