__all__ = ()

from ..user_balance import (
    ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST, USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE,
    register_user_balance_allocation_hook
)

from .relationship_request_queries import get_relationship_request


def get_allocation_aliveness(session_id, data):
    """
    Returns whether such an allocation is alive.
    
    Parameters
    ----------
    session_id : `int`
        The session's identifier.
    
    data : `None`
        Additional data.
    
    Returns
    -------
    aliveness : `int`
    """
    return USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE


async def get_session_entry(session_id):
    """
    Returns the session's entry.
    
    This function is a coroutine.
    
    Parameters
    ----------
    session_id : `int`
        The session's identifier.
    
    Returns
    -------
    session_entry : ``None | MarketPlaceItem``
    """
    return await get_relationship_request(session_id)


register_user_balance_allocation_hook(
    ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST,
    get_allocation_aliveness,
    get_session_entry,
)
