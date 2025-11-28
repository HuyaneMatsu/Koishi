from types import FunctionType

import vampytest

from ..user_balance_allocation_hook import UserBalanceAllocationHook


def _assert_fields_set(user_balance_allocation_hook):
    """
    Asserts whether every fields are set.
    
    Parameters
    ----------
    user_balance_allocation_hook : ``UserBalanceAllocationHook``
        The instance to check.
    """
    vampytest.assert_instance(user_balance_allocation_hook, UserBalanceAllocationHook)
    vampytest.assert_instance(user_balance_allocation_hook.allocation_feature_id, int)
    vampytest.assert_instance(user_balance_allocation_hook.is_allocation_alive_sync, FunctionType, nullable = True)
    vampytest.assert_instance(user_balance_allocation_hook.get_session_enty, FunctionType, nullable = True)


def test__UserBalanceAllocationHook__new():
    """
    Tests whether ``UserBalanceAllocationHook.__new__`` works as intended.
    """
    allocation_feature_id = 9999
    def is_allocation_alive_sync(session_id):
        return False
    
    async def get_session_enty(session_id):
        return None
    
    user_balance_allocation_hook = UserBalanceAllocationHook(
        allocation_feature_id,
        is_allocation_alive_sync,
        get_session_enty,
    )
    
    _assert_fields_set(user_balance_allocation_hook)
    vampytest.assert_eq(user_balance_allocation_hook.allocation_feature_id, allocation_feature_id)
    vampytest.assert_is(user_balance_allocation_hook.is_allocation_alive_sync, is_allocation_alive_sync)
    vampytest.assert_is(user_balance_allocation_hook.get_session_enty, get_session_enty)


def test__UserBalanceAllocationHook__repr():
    """
    Tests whether ``UserBalanceAllocationHook.__new__`` works as intended.
    """
    allocation_feature_id = 9999
    def is_allocation_alive_sync(session_id):
        return False
    
    async def get_session_enty(session_id):
        return None
    
    user_balance_allocation_hook = UserBalanceAllocationHook(
        allocation_feature_id,
        is_allocation_alive_sync,
        get_session_enty,
    )
    
    output = repr(user_balance_allocation_hook)
    vampytest.assert_instance(output, str)
