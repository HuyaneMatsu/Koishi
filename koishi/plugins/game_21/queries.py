__all__ = ()

from math import floor

from ..user_balance import get_user_balance


async def modify_user_hearts(user_id, amount, multiplier, unallocate):
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
    
    unallocate : `bool`
        Whether the user's hearts should be unallocated.
    """
    user_balance = await get_user_balance(user_id)
    
    if multiplier:
        user_balance.set('balance', user_balance.balance + floor(amount * multiplier))
    
    if unallocate:
        user_balance.set('allocated', user_balance.allocated - amount)
    
    await user_balance.save()


async def batch_modify_user_hearts(items):
    """
    Modifies multiple user's hearts.
    
    This function is a coroutine.
    
    Parameters
    ----------
    items : `list<(int, int, int, bool)>`
        The `user_id`, `amount`, `increase`, `unallocate` as a tuple.
    """
    for item in items:
        await modify_user_hearts(*item)
