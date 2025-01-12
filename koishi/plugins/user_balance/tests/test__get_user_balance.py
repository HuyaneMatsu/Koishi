from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import KOKORO
from scarletio import Future, Task, skip_ready_cycle

from ..constants import USER_BALANCE_CACHE, USER_BALANCE_QUERY_TASKS
from ..queries import get_user_balance
from ..user_balance import UserBalance


async def test__get_user_balance__cached():
    """
    Tests whether ``get_user_balance`` works as intended.
    
    Case: cached.
    """
    user_id_0 = 202412070040
    user_id_1 = 202412070041
    
    async def mocked_query_user_balance(user_id, waiters):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_user_balance,
        query_user_balance = mocked_query_user_balance,
        recursion = 2
    )
    
    try:
        user_balance_0 = UserBalance(user_id_0)
        user_balance_1 = UserBalance(user_id_1)
        
        USER_BALANCE_CACHE[user_id_0] = user_balance_0
        USER_BALANCE_CACHE[user_id_1] = user_balance_1
        
        vampytest.assert_eq(
            [*USER_BALANCE_CACHE.keys()],
            [user_id_0, user_id_1],
        )
        
        output = await mocked(user_id_0)
        vampytest.assert_instance(output, UserBalance)
        vampytest.assert_is(output, user_balance_0)
        
        vampytest.assert_eq(
            [*USER_BALANCE_CACHE.keys()],
            [user_id_1, user_id_0],
        )
        
    finally:
        USER_BALANCE_CACHE.clear()


async def test__get_user_balance__request():
    """
    Tests whether ``get_user_balance`` works as intended.
    
    Case: requesting.
    """
    allocated = 50
    balance = 51
    count_daily_by_related = 52
    count_daily_for_related = 53
    count_daily_self = 54
    count_top_gg_vote = 55
    daily_can_claim_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    daily_reminded = True
    entry_id = 1100
    streak = 56
    top_gg_voted_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    user_id = 202412070043
    relationship_value = 57
    relationship_divorces = 58
    relationship_slots = 59
    
    user_balance = None
    
    entry = {
        'allocated': allocated,
        'balance': balance,
        'count_daily_by_related': count_daily_by_related,
        'count_daily_for_related': count_daily_for_related,
        'count_daily_self': count_daily_self,
        'count_top_gg_vote': count_top_gg_vote,
        'daily_can_claim_at': daily_can_claim_at.replace(tzinfo = None),
        'daily_reminded': daily_reminded,
        'id': entry_id,
        'streak': streak,
        'top_gg_voted_at': top_gg_voted_at.replace(tzinfo = None),
        'user_id': user_id,
        'relationship_value': relationship_value,
        'relationship_divorces': relationship_divorces,
        'relationship_slots': relationship_slots,
    }
    
    async def mocked_query_user_balance(input_user_id, waiters):
        nonlocal entry
        nonlocal user_id
        nonlocal user_balance
        
        try:
            vampytest.assert_eq(input_user_id, user_id)
            vampytest.assert_instance(waiters, list)
            for element in waiters:
                vampytest.assert_instance(element, Future)
            
            user_balance = UserBalance.from_entry(entry)
            for waiter in waiters:
                waiter.set_result_if_pending(user_balance)
        finally:
            try:
                del USER_BALANCE_QUERY_TASKS[user_id]
            except KeyError:
                pass
    
    
    mocked = vampytest.mock_globals(
        get_user_balance,
        query_user_balance = mocked_query_user_balance,
        recursion = 2
    )
    
    task_0 = None
    task_1 = None
    
    try:
        task_0 = Task(KOKORO, mocked(user_id))
        task_0.apply_timeout(0.1)
        task_1 = Task(KOKORO, mocked(user_id))
        task_1.apply_timeout(0.1)
        
        vampytest.assert_eq(
            [*USER_BALANCE_CACHE.keys()],
            [],
        )
        
        vampytest.assert_false(USER_BALANCE_QUERY_TASKS)
        
        await skip_ready_cycle()
        
        vampytest.assert_true(USER_BALANCE_QUERY_TASKS)
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is_not(user_balance, None)
        vampytest.assert_is(user_balance, output_0)
        vampytest.assert_is(user_balance, output_1)
        
        vampytest.assert_eq(
            [*USER_BALANCE_CACHE.keys()],
            [user_id],
        )
        vampytest.assert_false(USER_BALANCE_QUERY_TASKS)
        
    finally:
        USER_BALANCE_CACHE.clear()
        USER_BALANCE_QUERY_TASKS.clear()
        
        if (task_0 is not None):
            task_0.cancel()
        
        if (task_1 is not None):
            task_1.cancel()
