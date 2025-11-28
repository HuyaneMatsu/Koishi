__all__ = ()

from math import floor

from ..user_balance import ALLOCATION_FEATURE_ID_GAME_21, get_user_balance, save_user_balance


async def modify_user_hearts(user_id, amount, multiplier, session_id):
    """
    Modifies the amount of hearts a user has.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The owner user's identifier.
    
    amount : `int`
        The amount to allocate.
    
    multiplier : `int`
        Whether to increase the user's or decrease. Can be `0` if it should not be modified.
    
    session_id : `int`
        The session's identifier to unallocate.
    """
    user_balance = await get_user_balance(user_id)
    
    if multiplier:
        user_balance.modify_balance_by(floor(amount * multiplier))
    
    if session_id:
        user_balance.remove_allocation(ALLOCATION_FEATURE_ID_GAME_21, session_id)
    
    await save_user_balance(user_balance)


async def batch_modify_user_hearts(items, session_id):
    """
    Modifies multiple user's hearts.
    
    This function is a coroutine.
    
    Parameters
    ----------
    items : `list<(int, int, bool)>`
        The `user_id`, `amount`, `multiplier` as a tuple.
    
    session_id : `int`
        The session's identifier to unallocate.
    """
    for item in items:
        await modify_user_hearts(*item, session_id)
