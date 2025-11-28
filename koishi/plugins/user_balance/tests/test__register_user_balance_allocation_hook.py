import vampytest

from ..user_balance_allocation_hook import UserBalanceAllocationHook
from ..utils import register_user_balance_allocation_hook


def test__register_user_balance_allocation_hook():
    """
    Tests whether ``register_user_balance_allocation_hook`` works as intended.
    """
    allocation_feature_id = 9999
    is_allocation_alive_sync = None
    get_session_enty = None
    
    hooks_patched = {}
    
    mocked = vampytest.mock_globals(
        register_user_balance_allocation_hook,
        USER_BALANCE_ALLOCATION_HOOKS = hooks_patched
    )
    
    output = mocked(
        allocation_feature_id,
        is_allocation_alive_sync,
        get_session_enty,
    )
    
    vampytest.assert_instance(output, UserBalanceAllocationHook)
    vampytest.assert_eq(output.allocation_feature_id, allocation_feature_id)
    vampytest.assert_eq(hooks_patched, {allocation_feature_id : output})
