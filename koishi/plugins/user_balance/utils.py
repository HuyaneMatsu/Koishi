__all__ = ('register_user_balance_allocation_hook',)

from .constants import USER_BALANCE_ALLOCATION_HOOKS
from .user_balance_allocation_hook import UserBalanceAllocationHook


def register_user_balance_allocation_hook(allocation_feature_id, is_allocation_alive_sync, get_session_enty):
    """
    Registers and returns the new hook.
    
    Parameters
    ----------
    allocation_feature_id : `int`
        The allocation feature's identifier.
    
    is_allocation_alive_sync : `None | FunctionType`
        Sync check whether the allocation is alive.
    
    get_session_enty : `None | CoroutineFunction`
        A function to get the session's entry.
    
    Returns
    -------
    user_balance_allocation_hook : ``UserBalanceAllocationHook``
    """
    user_balance_allocation_hook = UserBalanceAllocationHook(
        allocation_feature_id,
        is_allocation_alive_sync,
        get_session_enty,
    )
    USER_BALANCE_ALLOCATION_HOOKS[allocation_feature_id] = user_balance_allocation_hook
    return user_balance_allocation_hook
