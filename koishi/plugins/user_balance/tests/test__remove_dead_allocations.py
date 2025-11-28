import vampytest

from ....bot_utils.models import DB_ENGINE

from ..queries import remove_dead_allocations
from ..user_balance import UserBalance
from ..user_balance_allocation_hook import UserBalanceAllocationHook


@vampytest.skip_if(DB_ENGINE is not None)
async def test__remove_dead_allocations():
    """
    Tests whether ``remove_dead_allocations`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202511220000
    
    allocation_feature_id_0 = 5911
    allocation_feature_id_1 = 5921
    
    allocation_hooks = {
        allocation_feature_id_0 : UserBalanceAllocationHook(
            allocation_feature_id_0,
            (lambda session_id : session_id == 5666),
            None,
        ),
    }
    
    allocation_0 = (
        allocation_feature_id_0,
        568,
        1,
    )
    
    allocation_1 = (
        allocation_feature_id_0,
        5666,
        2,
    )
    
    allocation_2 = (
        allocation_feature_id_1,
        1242424,
        666,
    )
    
    user_balance = UserBalance(user_id)
    user_balance.add_allocation(*allocation_0)
    user_balance.add_allocation(*allocation_1)
    user_balance.add_allocation(*allocation_2)
    
    mocked = vampytest.mock_globals(
        remove_dead_allocations,
        USER_BALANCE_ALLOCATION_HOOKS = allocation_hooks,
    )
    await mocked(user_balance)
    
    vampytest.assert_eq(
        [*user_balance.iter_allocations()],
        [
            allocation_1,
        ],
    )
