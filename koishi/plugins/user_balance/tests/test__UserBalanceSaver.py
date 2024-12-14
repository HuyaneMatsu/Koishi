import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..user_balance import UserBalance
from ..user_balance_saver import UserBalanceSaver
from ..constants import USER_BALANCE_CACHE


def _assert_fields_set(user_balance_saver):
    """
    Tests whether every fields are set of the given automation configuration saver.
    
    Parameters
    ----------
    user_balance_saver : ``UserBalanceSaver``
        The instance to check.
    """
    vampytest.assert_instance(user_balance_saver, UserBalanceSaver)
    vampytest.assert_instance(user_balance_saver.entry_proxy, UserBalance)
    vampytest.assert_instance(user_balance_saver.ensured_for_deletion, bool)
    vampytest.assert_instance(user_balance_saver.modified_fields, dict, nullable = True)
    vampytest.assert_instance(user_balance_saver.run_task, Task, nullable = True)


def test__UserBalanceSaver__new():
    """
    Tests whether ``UserBalanceSaver.__new__`` works as intended.
    """
    user_id = 202412070015
    
    try:
        user_balance = UserBalance(user_id)
        
        user_balance_saver = UserBalanceSaver(user_balance)
        _assert_fields_set(user_balance_saver)
        
        vampytest.assert_is(user_balance_saver.entry_proxy, user_balance)

    finally:
        USER_BALANCE_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserBalanceSaver__repr():
    """
    Tests whether ``UserBalanceSaver.__repr__`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202412070016
    
    old_streak = 56
    
    new_streak = 'nyan'
    
    try:
        user_balance = UserBalance(user_id)
        user_balance.streak = old_streak
        
        ensured_for_deletion = True
        modified_fields = {'streak': new_streak}
        
        user_balance_saver = UserBalanceSaver(user_balance)
        user_balance_saver.ensured_for_deletion = ensured_for_deletion
        user_balance_saver.modified_fields = modified_fields
        user_balance_saver.run_task = Task(get_event_loop(), user_balance_saver.run())
        
        output = repr(user_balance_saver)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(UserBalanceSaver.__name__, output)
        vampytest.assert_in(f'entry_proxy = {user_balance!r}', output)
        vampytest.assert_in(f'ensured_for_deletion = {ensured_for_deletion!r}', output)
        vampytest.assert_in(f'modified_fields = {modified_fields!r}', output)
        vampytest.assert_in(f'running = {True!r}', output)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalanceSaver__add_modification():
    """
    Tests whether ``UserBalanceSaver.add_modification`` works as intended.
    """
    user_id = 202412070017
    
    old_streak = 56
    old_waifu_cost = 20
    
    new_streak = 'nyan'
    new_waifu_cost = 'hey mister'
    
    try:
        user_balance = UserBalance(user_id)
        user_balance.streak = old_streak
        user_balance.waifu_cost = old_waifu_cost
        
        user_balance_saver = UserBalanceSaver(user_balance)
        
        vampytest.assert_eq(
            user_balance_saver.modified_fields,
            None,
        )
        
        user_balance_saver.add_modification('streak', new_streak)
        
        vampytest.assert_eq(
            user_balance_saver.modified_fields,
            {
                'streak': new_streak,
            }
        )
        
        user_balance_saver.add_modification('waifu_cost', new_waifu_cost)
        
        vampytest.assert_eq(
            user_balance_saver.modified_fields,
            {
                'streak': new_streak,
                'waifu_cost': new_waifu_cost,
            }
        )
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalanceSaver__ensure_deletion():
    """
    Tests whether ``UserBalanceSaver.ensure_deletion`` works as intended.
    """
    user_id = 202412070018
    
    try:
        user_balance = UserBalance(user_id)
        
        user_balance_saver = UserBalanceSaver(user_balance)
        
        vampytest.assert_eq(user_balance_saver.ensured_for_deletion, False)
        
        user_balance_saver.ensure_deletion()
        
        vampytest.assert_eq(user_balance_saver.ensured_for_deletion, True)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalanceSaver__is_modified__not():
    """
    Tests whether ``UserBalanceSaver.is_modified`` works as intended.
    
    Case: not modified.
    """
    user_id = 202412070019
    
    try:
        user_balance = UserBalance(user_id)
        
        user_balance_saver = UserBalanceSaver(user_balance)
        
        output = user_balance_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, False)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalanceSaver__is_modified__delete():
    """
    Tests whether ``UserBalanceSaver.is_modified`` works as intended.
    
    Case: ensured for deletion.
    """
    user_id = 202412070020
    
    try:
        user_balance = UserBalance(user_id)
        
        user_balance_saver = UserBalanceSaver(user_balance)
        user_balance_saver.ensure_deletion()
        
        output = user_balance_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalanceSaver__is_modified__field():
    """
    Tests whether ``UserBalanceSaver.is_modified`` works as intended.
    
    Case: field modified.
    """
    user_id = 202412070021
    
    old_streak = 56
    
    new_streak = 63
    
    try:
        user_balance = UserBalance(user_id)
        user_balance.streak = old_streak
        
        user_balance_saver = UserBalanceSaver(user_balance)
        user_balance_saver.add_modification('streak', new_streak)
        
        output = user_balance_saver.is_modified()
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        USER_BALANCE_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserBalanceSaver__begin():
    """
    Tests whether ``UserBalanceSaver.begin`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202412070022
    
    try:
        user_balance = UserBalance(user_id)
        
        user_balance_saver = UserBalanceSaver(user_balance)
        user_balance.saver = user_balance_saver
        
        output = user_balance_saver.begin()
        
        vampytest.assert_instance(output, Task)
        vampytest.assert_is(user_balance_saver.run_task, output)
        vampytest.assert_is(user_balance.saver, user_balance_saver)
        
        # do save
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        # after save nothing should be set.
        vampytest.assert_is(user_balance_saver.run_task, None)
        vampytest.assert_is(user_balance.saver, None)
    
    finally:
        USER_BALANCE_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def UserBalanceSaver__running():
    """
    Tests whether ``UserBalanceSaver.running`` works as intended.
    """
    user_id = 202412070023
    
    try:
        user_balance = UserBalance(user_id)
        
        user_balance_saver = UserBalanceSaver(user_balance)
        user_balance.saver = user_balance_saver
        
        output = user_balance_saver.running
        vampytest.assert_eq(output, False)
        
        user_balance_saver.begin()
        
        output = user_balance_saver.running
        vampytest.assert_eq(output, True)
        
    finally:
        USER_BALANCE_CACHE.clear()
