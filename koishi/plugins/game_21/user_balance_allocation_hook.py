__all__ = ()

from ..user_balance import ALLOCATION_FEATURE_ID_GAME_21, register_user_balance_allocation_hook

from .constants import SESSIONS


def is_allocation_alive_sync(session_id):
    """
    Returns whether such an allocation is alive.
    
    Parameters
    ----------
    session_id : `int`
        The session's identifier.
    
    Returns
    -------
    alive : `bool`
    """
    return session_id in SESSIONS


async def get_session_enty(session_id):
    """
    Returns the session's entry.
    
    This function is a coroutine.
    
    Parameters
    ----------
    session_id : `int`
        The session's identifier.
    
    Returns
    -------
    session_entry : ``Game21Session``
    """
    return SESSIONS.get(session_id, None)


register_user_balance_allocation_hook(
    ALLOCATION_FEATURE_ID_GAME_21,
    is_allocation_alive_sync,
    get_session_enty,
)
