__all__ = ()

from datetime import datetime as DateTime, timezone as TimeZone

from ..user_balance import (
    ALLOCATION_FEATURE_ID_MARKET_PLACE, USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE,
    USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_APPLY, register_user_balance_allocation_hook
)

from .queries import get_market_place_item


def get_allocation_aliveness(session_id, data):
    """
    Returns whether such an allocation is alive.
    
    Parameters
    ----------
    session_id : `int`
        The session's identifier.
    
    data : `bytes`
        Additional data.
    
    Returns
    -------
    aliveness : `int`
    """
    current_timestamp = DateTime.now(TimeZone.utc).timestamp()
    finalises_at = int.from_bytes(data, 'little')
    
    return (
        USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE
        if (current_timestamp < finalises_at) else
        USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_APPLY
    )


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
    session_entry : ``None | MarketPlaceItem``
    """
    return await get_market_place_item(session_id)


register_user_balance_allocation_hook(
    ALLOCATION_FEATURE_ID_MARKET_PLACE,
    get_allocation_aliveness,
    get_session_enty,
)
