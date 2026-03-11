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
    vampytest.assert_instance(user_balance_allocation_hook.get_allocation_aliveness, FunctionType, nullable = True)
    vampytest.assert_instance(user_balance_allocation_hook.get_session_entry, FunctionType, nullable = True)


def test__UserBalanceAllocationHook__new():
    """
    Tests whether ``UserBalanceAllocationHook.__new__`` works as intended.
    """
    allocation_feature_id = 9999
    def get_allocation_aliveness(session_id, data):
        return False
    
    async def get_session_entry(session_id):
        return None
    
    user_balance_allocation_hook = UserBalanceAllocationHook(
        allocation_feature_id,
        get_allocation_aliveness,
        get_session_entry,
    )
    
    _assert_fields_set(user_balance_allocation_hook)
    vampytest.assert_eq(user_balance_allocation_hook.allocation_feature_id, allocation_feature_id)
    vampytest.assert_is(user_balance_allocation_hook.get_allocation_aliveness, get_allocation_aliveness)
    vampytest.assert_is(user_balance_allocation_hook.get_session_entry, get_session_entry)


def test__UserBalanceAllocationHook__repr():
    """
    Tests whether ``UserBalanceAllocationHook.__new__`` works as intended.
    """
    allocation_feature_id = 9999
    def get_allocation_aliveness(session_id, data):
        return False
    
    async def get_session_entry(session_id):
        return None
    
    user_balance_allocation_hook = UserBalanceAllocationHook(
        allocation_feature_id,
        get_allocation_aliveness,
        get_session_entry,
    )
    
    output = repr(user_balance_allocation_hook)
    vampytest.assert_instance(output, str)
