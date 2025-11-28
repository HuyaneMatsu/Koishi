__all__ = ('get_user_balance', 'get_user_balances', 'save_user_balance')

from itertools import count

from hata import KOKORO
from scarletio import Future, Task, TaskGroup, copy_docs, shield

from ...bot_utils.models import DB_ENGINE, USER_BALANCE_TABLE, user_balance_model

from .constants import (
    USER_BALANCE_ALLOCATION_HOOKS, USER_BALANCE_CACHE, USER_BALANCE_QUERY_TASKS, USER_BALANCE_SAVE_TASKS, USER_BALANCES
)
from .user_balance import UserBalance


COUNTER = iter(count(1))


async def get_user_balance(user_id):
    """
    Gets the balance of the given user for their identifier.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    Returns
    -------
    user_balance : ``UserBalance``
    """
    user_balance = _get_user_balance_from_cache(user_id)
    if (user_balance is not None):
        return user_balance
    
    waiter = _get_user_balance_query_waiter(user_id)
    if waiter is None:
        waiter = _create_user_balance_query_waiter(user_id)
    
    return (await waiter)


async def get_user_balances(user_ids):
    """
    Gets the balance of the given user identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_ids : `iterable<int>`
        User identifiers.
    
    Returns
    -------
    user_balances : ``dict<int, UserBalance>``
    """
    user_balances = {}
    waiters = None
    user_ids_to_request = None
    
    for user_id in user_ids:
        user_balance = _get_user_balance_from_cache(user_id)
        if (user_balance is not None):
            user_balances[user_id] = user_balance
            continue
        
        # get waiter if available
        waiter = _get_user_balance_query_waiter(user_id)
        if (waiter is not None):
            if waiters is None:
                waiters = []
            waiters.append(waiter)
        
        # no waiter available, store for later.
        if user_ids_to_request is None:
            user_ids_to_request = []
        
        user_ids_to_request.append(user_id)
        continue
    
    if (user_ids_to_request is not None):
        if waiters is None:
            waiters = []
        
        waiters.extend(_create_user_balance_query_waiters(user_ids_to_request))
    
    if (waiters is not None):
        task_group = TaskGroup(KOKORO, waiters)
        with task_group.cancel_on_exception():
            async for waiter in task_group.exhaust():
                user_balance = waiter.get_result()
                user_balances[user_balance.user_id] = user_balance
    
    return user_balances


def _get_user_balance_from_cache(user_id):
    """
    Gets the user balance from cache.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to get the balance for.
    
    Returns
    -------
    user_balance : `None | UserBalance`
    """
    try:
        user_balance = USER_BALANCES[user_id]
    except KeyError:
        return None
    
    try:
        USER_BALANCE_CACHE.move_to_end(user_id)
    except KeyError:
        USER_BALANCE_CACHE[user_id] = user_balance
    
    return user_balance


def _get_user_balance_query_waiter(user_id):
    """
    Returns a user balance waiter. If there is no waiter yet, returns `None`.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to get the balance for.
    
    Returns
    -------
    waiter : `None | Future`
    """
    try:
        task, waiters = USER_BALANCE_QUERY_TASKS[user_id]
    except KeyError:
        return None
    
    waiter = Future(KOKORO)
    waiters.append(waiter)
    return waiter


def _create_user_balance_query_waiter(user_id):
    """
    Creates a user balance query waiter. Use it after `_get_user_balance_query_waiter`.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to get the balance for.
    
    Returns
    -------
    waiter : `Future`
    """
    waiters = []
    task = Task(KOKORO, query_user_balance(user_id, waiters))
    USER_BALANCE_QUERY_TASKS[user_id] = (task, waiters)
    waiter = Future(KOKORO)
    waiters.append(waiter)
    return waiter


def _create_user_balance_query_waiters(user_ids):
    """
    Creates user balance query waiters.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_ids : `list<int>`
        User identifier to get the balance for.
    
    Yields
    ------
    waiter : `Future`
    """
    items = [(user_id, []) for user_id in user_ids]
    task = Task(KOKORO, query_user_balances(items))
    
    for user_id, waiters in items:
        USER_BALANCE_QUERY_TASKS[user_id] = (task, waiters)
        waiter = Future(KOKORO)
        waiters.append(waiter)
        yield waiter


async def query_user_balance(user_id, waiters):
    """
    Requests the to user balance entries from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier to query for.
    
    waiters : `list<Future>`
        Result waiters.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                USER_BALANCE_TABLE.select().where(
                    user_balance_model.user_id == user_id,
                ),
            )
            
            result = await response.fetchone()
            if result is None:
                user_balance = UserBalance(user_id)
            else:
                user_balance = UserBalance.from_entry(result)
                await remove_dead_allocations(user_balance)
            
            USER_BALANCES[user_id] = user_balance
            USER_BALANCE_CACHE[user_id] = user_balance
            
    except BaseException as exception:
        for waiter in waiters:
            waiter.set_exception_if_pending(exception)
        raise
    
    else:
        for waiter in waiters:
            waiter.set_result_if_pending(user_balance)
    
    finally:
        try:
            del USER_BALANCE_QUERY_TASKS[user_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_user_balance)
    async def query_user_balance(user_id, waiters):
        try:
            user_balance = UserBalance(user_id)
            
            for waiter in waiters:
                waiter.set_result_if_pending(user_balance)
        
            USER_BALANCES[user_id] = user_balance
            USER_BALANCE_CACHE[user_id] = user_balance
        
        finally:
            try:
                del USER_BALANCE_QUERY_TASKS[user_id]
            except KeyError:
                pass


async def query_user_balances(items):
    """
    Requests the user balance entries from the database.
    
    This function is a coroutine.
    
    Parameters
    ----------
    items : `list<(int, list<Future>>`
        A list of user's identifier and result waiter pairs.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            response = await connector.execute(
                USER_BALANCE_TABLE.select().where(
                    user_balance_model.user_id.in_([item[0] for item in items]),
                ),
            )
            
            results = await response.fetchall()
            
            user_balances = {}
            
            for result in results:
                user_balance = UserBalance.from_entry(result)
                user_balances[user_balance.user_id] = user_balance
    
    except BaseException as exception:
        for item in items:
            waiters = item[1]
            for waiter in waiters:
                waiter.set_exception_if_pending(exception)
        raise
    
    else:
        for user_id, waiters in items:
            try:
                user_balance = user_balances[user_id]
            except KeyError:
                user_balance = UserBalance(user_id)
            else:
                await remove_dead_allocations(user_balance)
            
            USER_BALANCES[user_id] = user_balance
            USER_BALANCE_CACHE[user_id] = user_balance
            
            for waiter in waiters:
                waiter.set_result_if_pending(user_balance)
    
    finally:
        for item in items:
            user_id = item[0]
            try:
                del USER_BALANCE_QUERY_TASKS[user_id]
            except KeyError:
                pass


if (DB_ENGINE is None):
    @copy_docs(query_user_balance)
    async def query_user_balances(items):
        try:
            for user_id, waiters in items:
                user_balance = UserBalance(user_id)
                
                USER_BALANCES[user_id] = user_balance
                USER_BALANCE_CACHE[user_id] = user_balance
                
                for waiter in waiters:
                    waiter.set_result_if_pending(user_balance)
        
        finally:
            for item in items:
                user_id = item[0]
                try:
                    del USER_BALANCE_QUERY_TASKS[user_id]
                except KeyError:
                    pass


async def remove_dead_allocations(user_balance):
    """
    Removes the dead allocations hooks from the given user balance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to check.
    """
    to_remove = None
    
    for allocation_feature_id, allocation_session_id, amount in user_balance.iter_allocations():
        while True:
            try:
                user_balance_allocation_hook = USER_BALANCE_ALLOCATION_HOOKS[allocation_feature_id]
            except KeyError:
                do_remove = True
                break
            
            is_allocation_alive_sync = user_balance_allocation_hook.is_allocation_alive_sync
            if is_allocation_alive_sync is None:
                do_remove = True
                break
            
            if not is_allocation_alive_sync(allocation_session_id):
                do_remove = True
                break
            
            do_remove = False
            break
        
        if not do_remove:
            continue
        
        if to_remove is None:
            to_remove = []
        
        to_remove.append((allocation_feature_id, allocation_session_id))
        continue
    
    if to_remove is None:
        return
    
    for allocation_feature_id, allocation_session_id in reversed(to_remove):
        user_balance.remove_allocation(allocation_feature_id, allocation_session_id)
    
    await save_user_balance(user_balance)
    return


async def save_user_balance(user_balance):
    """
    Saves the user balance.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to save.
    """
    try:
        task = USER_BALANCE_SAVE_TASKS[user_balance.user_id]
    except KeyError:
        USER_BALANCE_SAVE_TASKS[user_balance.user_id] = task = Task(KOKORO, query_save_user_balance_loop(user_balance))
    
    await shield(task, KOKORO)


async def query_save_user_balance_loop(user_balance):
    """
    Runs the entry proxy saver.
    
    This method is a coroutine.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        User balance to save.
    """
    try:
        async with DB_ENGINE.connect() as connector:
            entry_id = user_balance.entry_id
            # Entry new that is all
            if (entry_id == 0):
                user_balance.modified_fields = None
                response = await connector.execute(
                    USER_BALANCE_TABLE.insert().values(
                        user_id = user_balance.user_id,
                        allocations = user_balance.allocations,
                        balance = user_balance.balance,
                        count_daily_self = user_balance.count_daily_self,
                        count_daily_by_related = user_balance.count_daily_by_related,
                        count_daily_for_related = user_balance.count_daily_for_related,
                        count_top_gg_vote = user_balance.count_top_gg_vote,
                        top_gg_voted_at = user_balance.top_gg_voted_at,
                        daily_can_claim_at = user_balance.daily_can_claim_at,
                        daily_reminded = user_balance.daily_reminded,
                        streak = user_balance.streak,
                        relationship_value = user_balance.relationship_value,
                        relationship_divorces = user_balance.relationship_divorces,
                        relationship_slots = user_balance.relationship_slots,
                    ).returning(
                        user_balance_model.id,
                    )
                )
                
                result = await response.fetchone()
                user_balance.entry_id = result[0]
            
            modified_fields = user_balance.modified_fields
            while (modified_fields is not None):
                user_balance.modified_fields = None
                
                await connector.execute(
                    USER_BALANCE_TABLE.update(
                        user_balance_model.id == entry_id,
                    ).values(
                        **modified_fields
                    )
                )
                modified_fields = user_balance.modified_fields
                continue
        
    finally:
        try:
            del USER_BALANCE_SAVE_TASKS[user_balance.user_id]
        except KeyError:
            pass


if (DB_ENGINE is None):
    @copy_docs(query_save_user_balance_loop)
    async def query_save_user_balance_loop(user_balance):
        user_balance.modified_fields = None
        if not user_balance.entry_id:
            user_balance.entry_id = next(COUNTER)
