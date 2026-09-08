import vampytest

from ..constants import USER_BALANCE_CACHE, USER_BALANCES
from ..queries import user_balance_get_many
from ..user_balance import user_balance_create


async def test__user_balance_get_many__cached():
    """
    Tests whether ``user_balance_get_many`` works as intended.
    
    Case: cached.
    """
    user_id_0 = 202412080040
    user_id_1 = 202412080041
    
    async def mocked_query_user_balance(user_id, waiters):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        user_balance_get_many,
        query_user_balance = mocked_query_user_balance,
        recursion = 2
    )
    
    try:
        user_balance_0 = user_balance_create(user_id_0)
        user_balance_1 = user_balance_create(user_id_1)
        
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
