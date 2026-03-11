__all__ = ()

from ..user_balance import (
    ALLOCATION_FEATURE_ID_GAME_21, USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE,
    USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_DELETE,register_user_balance_allocation_hook
)

from .constants import SESSIONS


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
    return (
        USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE
        if (session_id in SESSIONS) else
        USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_DELETE
    )


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
    session_entry : ``None | Game21Session``
    """
    return SESSIONS.get(session_id, None)


register_user_balance_allocation_hook(
    ALLOCATION_FEATURE_ID_GAME_21,
    get_allocation_aliveness,
    get_session_entry,
)
