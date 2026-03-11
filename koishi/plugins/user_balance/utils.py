__all__ = ('register_user_balance_allocation_hook',)

from .constants import USER_BALANCE_ALLOCATION_HOOKS
from .user_balance_allocation_hook import UserBalanceAllocationHook


def register_user_balance_allocation_hook(allocation_feature_id, get_allocation_aliveness, get_session_entry):
    """
    Registers and returns the new hook.
    
    Parameters
    ----------
    allocation_feature_id : `int`
        The allocation feature's identifier.
    
    get_allocation_aliveness : `None | FunctionType`
        Sync check whether the allocation is alive.
    
    get_session_entry : `None | CoroutineFunction`
        A function to get the session's entry.
    
    Returns
    -------
    user_balance_allocation_hook : ``UserBalanceAllocationHook``
    """
    user_balance_allocation_hook = UserBalanceAllocationHook(
        allocation_feature_id,
        get_allocation_aliveness,
        get_session_entry,
    )
    USER_BALANCE_ALLOCATION_HOOKS[allocation_feature_id] = user_balance_allocation_hook
    return user_balance_allocation_hook
