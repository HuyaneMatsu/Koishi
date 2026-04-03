import vampytest

from ..constants import USER_BALANCE_CACHE, USER_BALANCES
from ..queries import get_user_balances
from ..user_balance import UserBalance


async def test__get_user_balances__cached():
    """
    Tests whether ``get_user_balances`` works as intended.
    
    Case: cached.
    """
    user_id_0 = 202412080040
    user_id_1 = 202412080041
    
    async def mocked_query_user_balance(user_id, waiters):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_user_balances,
        query_user_balance = mocked_query_user_balance,
        recursion = 2
    )
    
    try:
        user_balance_0 = UserBalance(user_id_0)
        user_balance_1 = UserBalance(user_id_1)
        
        USER_BALANCES[user_id_0] = user_balance_0
        USER_BALANCES[user_id_1] = user_balance_1
        
        USER_BALANCE_CACHE[user_id_0] = user_balance_0
        USER_BALANCE_CACHE[user_id_1] = user_balance_1
        
        vampytest.assert_eq(
            [*USER_BALANCE_CACHE.keys()],
            [user_id_0, user_id_1],
        )
        
        output = await mocked((user_id_0, user_id_1),)
        vampytest.assert_instance(output, dict)
        vampytest.assert_eq(output, {user_id_0: user_balance_0, user_id_1: user_balance_1})
        
        vampytest.assert_eq(
            {*USER_BALANCES.keys()},
            {user_id_0, user_id_1},
        )
        
        vampytest.assert_eq(
            [*USER_BALANCE_CACHE.keys()],
            [user_id_0, user_id_1],
        )
        
    finally:
        USER_BALANCES.clear()
        USER_BALANCE_CACHE.clear()
