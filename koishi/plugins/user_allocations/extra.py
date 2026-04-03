__all__ = ()

from ..user_balance import ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST

from .extra_relationship_request import get_relationship_request_entry_extra


async def get_extra(user_id, allocation_feature_id, session_id, amount, session):
    """
    Gets extra data for building detailed component.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    allocation_feature_id : `int`
        The allocation feature's identifier.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    session : `None | object`
        The game's session.
    
    Returns
    -------
    extra : `None | object`
    """
    if allocation_feature_id == ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST:
        extra_getter = get_relationship_request_entry_extra
    else:
        extra_getter = None
    
    if extra_getter is None:
        extra = None
    else:
        extra = await extra_getter(user_id, session_id, amount, session)
    
    return extra
