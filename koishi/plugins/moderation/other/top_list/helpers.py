__all__ = ()

from math import floor, log10

from .....bot_utils.user_getter import get_user

from ...shared_constants import REASON_RP


async def get_source_user_from_client_entry(entry):
    """
    Gets the source invoker user if the client executed an action.
    
    This function is a coroutine.
    
    Parameters
    ----------
    entry : ``AuditLogEntry``
        The entry to inspect.
    
    Returns
    -------
    source_user : `None`, ``ClientUserBase``
    """
    reason = entry.reason
    if (reason is None):
        return None
    
    match = REASON_RP.fullmatch(reason)
    if match is None:
        return None
    
    user_id = int(match.group(1))
    return await get_user(user_id)


def get_integer_length(value):
    """
    Gets an integer's length.
    
    Parameters
    ----------
    value : `int`
        The value to get its length of.
    
    Returns
    -------
    length : `int`
    """
    if not value:
        return 1
    
    return floor(log10(value)) + 1
