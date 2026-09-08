import vampytest

from ....bot_utils.models import DB_ENGINE

from ..constants import (
    USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE, USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_APPLY,
    USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_DELETE
)
from ..queries import remove_dead_allocations
from ..user_balance import (
    user_balance_add_allocation, user_balance_create, user_balance_iter_allocations, user_balance_modify_balance_by
)
from ..user_balance_allocation_hook import UserBalanceAllocationHook


@vampytest.skip_if(DB_ENGINE is not None)
async def test__remove_dead_allocations():
    """
    Tests whether ``remove_dead_allocations`` works as intended.
    
    This function is a coroutine.
    
    Case: remove
    """
    user_id = 202511220000
    
    allocation_feature_id_0 = 5911
    allocation_feature_id_1 = 5921
    allocation_feature_id_2 = 5922
    
    allocation_hooks = {
        allocation_feature_id_0 : UserBalanceAllocationHook(
            allocation_feature_id_0,
            (lambda session_id, data: (
                USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE
                if (session_id == 5666) else
                USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_DELETE)
            ),
            None,
        ),
        allocation_feature_id_2 : UserBalanceAllocationHook(
            allocation_feature_id_2,
            (lambda session_id, data: (
                USER_BALANCE_ALLOCATION_ALIVENESS_ALIVE
                if (session_id == 5666) else
                USER_BALANCE_ALLOCATION_ALIVENESS_DEAD_APPLY)
            ),
            None,
        ),
    }
    
    allocation_0 = (
        allocation_feature_id_0,
        568,
        1,
        None,
    )
    
    allocation_1 = (
        allocation_feature_id_0,
        5666,
        2,
        None,
    )
    
    allocation_2 = (
        allocation_feature_id_1,
        1242424,
        666,
        None,
    )
    
    allocation_3 = (
        allocation_feature_id_2,
        12,
        200,
        None,
    )
    
    user_balance = user_balance_create(user_id)
    user_balance_modify_balance_by(user_balance, 1000)
    user_balance_add_allocation(user_balance, *allocation_0)
    user_balance_add_allocation(user_balance, *allocation_1)
    user_balance_add_allocation(user_balance, *allocation_2)
    user_balance_add_allocation(user_balance, *allocation_3)
    
    mocked = vampytest.mock_globals(
        remove_dead_allocations,
        USER_BALANCE_ALLOCATION_HOOKS = allocation_hooks,
    )
    await mocked(user_balance)
    
    vampytest.assert_eq(
        [*user_balance_iter_allocations(user_balance)],
        [
            allocation_1,
        ],
    )
    vampytest.assert_eq(user_balance.balance, 800)
