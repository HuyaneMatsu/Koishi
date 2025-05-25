from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import DATETIME_FORMAT_CODE
from scarletio import Task, get_event_loop, skip_ready_cycle

from ....bot_utils.models import DB_ENGINE

from ..constants import USER_BALANCE_CACHE
from ..user_balance import UserBalance
from ..user_balance_saver import UserBalanceSaver


def _assert_fields_set(user_balance):
    """
    Asserts whether every fields are set of the user balance.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        The user balance to test.
    """
    vampytest.assert_instance(user_balance, UserBalance)
    vampytest.assert_instance(user_balance.allocated, int)
    vampytest.assert_instance(user_balance.count_daily_by_related, int)
    vampytest.assert_instance(user_balance.count_daily_for_related, int)
    vampytest.assert_instance(user_balance.count_daily_self, int)
    vampytest.assert_instance(user_balance.count_top_gg_vote, int)
    vampytest.assert_instance(user_balance.daily_can_claim_at, DateTime)
    vampytest.assert_instance(user_balance.daily_reminded, bool)
    vampytest.assert_instance(user_balance.streak, int)
    vampytest.assert_instance(user_balance.entry_id, int)
    vampytest.assert_instance(user_balance.top_gg_voted_at, DateTime)
    vampytest.assert_instance(user_balance.relationship_value, int)
    vampytest.assert_instance(user_balance.relationship_divorces, int)
    vampytest.assert_instance(user_balance.relationship_slots, int)
    vampytest.assert_instance(user_balance.user_id, int)


def test__UserBalance__new():
    """
    Tests whether ``UserBalance.__new__`` works as intended.
    """
    user_id = 202412070000
    
    try:
        user_balance = UserBalance(user_id)
        _assert_fields_set(user_balance)
        
        vampytest.assert_eq(user_balance.user_id, user_id)
        
        # Should not auto store in cache
        vampytest.assert_is(USER_BALANCE_CACHE.get(user_balance.entry_id, None), None)
        
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalance__repr():
    """
    Tests whether ``user_balance.__repr__`` works as intended.
    """
    allocated = 7
    balance = 8
    count_daily_by_related = 9
    count_daily_for_related = 10
    count_daily_self = 11
    count_top_gg_vote = 12
    daily_can_claim_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    daily_reminded = True
    entry_id = 1020
    streak = 13
    top_gg_voted_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    user_id = 202412070001
    relationship_value = 14
    relationship_divorces = 15
    relationship_slots = 16
    
    try:
        
        user_balance = UserBalance(user_id)
        user_balance.allocated = allocated
        user_balance.balance = balance
        user_balance.count_daily_by_related = count_daily_by_related
        user_balance.count_daily_for_related = count_daily_for_related
        user_balance.count_daily_self = count_daily_self
        user_balance.count_top_gg_vote = count_top_gg_vote
        user_balance.daily_can_claim_at = daily_can_claim_at
        user_balance.daily_reminded = daily_reminded
        user_balance.streak = streak
        user_balance.entry_id = entry_id
        user_balance.top_gg_voted_at = top_gg_voted_at
        user_balance.relationship_value = relationship_value
        user_balance.relationship_divorces = relationship_divorces
        user_balance.relationship_slots = relationship_slots
        
        user_balance.entry_id = entry_id
        
        output = repr(user_balance)
        
        vampytest.assert_instance(output, str)
        
        vampytest.assert_in(UserBalance.__name__, output)
        vampytest.assert_in(f'allocated = {allocated!r}', output)
        vampytest.assert_in(f'balance = {balance!r}', output)
        vampytest.assert_in(f'count_daily_by_related = {count_daily_by_related!r}', output)
        vampytest.assert_in(f'count_daily_for_related = {count_daily_for_related!r}', output)
        vampytest.assert_in(f'count_daily_self = {count_daily_self!r}', output)
        vampytest.assert_in(f'count_top_gg_vote = {count_top_gg_vote!r}', output)
        vampytest.assert_in(f'daily_can_claim_at = {daily_can_claim_at:{DATETIME_FORMAT_CODE}}', output)
        vampytest.assert_in(f'daily_reminded = {daily_reminded!r}', output)
        vampytest.assert_in(f'streak = {streak!r}', output)
        vampytest.assert_in(f'entry_id = {entry_id!r}', output)
        vampytest.assert_in(f'user_id = {user_id!r}', output)
        vampytest.assert_in(f'top_gg_voted_at = {top_gg_voted_at:{DATETIME_FORMAT_CODE}}', output)
        vampytest.assert_in(f'relationship_value = {relationship_value!r}', output)
        vampytest.assert_in(f'relationship_divorces = {relationship_divorces!r}', output)
        vampytest.assert_in(f'relationship_slots = {relationship_slots!r}', output)
        
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalance__bool():
    """
    Tests whether ``UserBalance.__bool__`` works as intended.
    
    Returns
    -------
    output : `bool`
    """
    user_id = 202412070004
    
    try:
        user_balance = UserBalance(user_id)
        
        output = bool(user_balance)
        vampytest.assert_instance(output, bool)
        vampytest.assert_eq(output, True)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalance__get_saver():
    """
    Tests whether ``UserBalance.get_saver`` works as intended.
    """
    user_id = 202412070005
    
    try:
        user_balance = UserBalance(user_id)
        
        output = user_balance.get_saver()
        vampytest.assert_instance(output, UserBalanceSaver)
        vampytest.assert_is(output.entry_proxy, user_balance)
        vampytest.assert_is(user_balance.saver, output)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalance__get_saver__caching():
    """
    Tests whether ``UserBalance.get_saver`` works as intended.
    
    Case: caching.
    """
    user_id = 202412070006
    
    try:
        user_balance = UserBalance(user_id)
        
        output_0 = user_balance.get_saver()
        output_1 = user_balance.get_saver()
        vampytest.assert_is(output_0, output_1)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalance__from_entry():
    """
    Tests whether ``UserBalance.from_entry`` works as intended.
    """
    allocated = 20
    balance = 21
    count_daily_by_related = 22
    count_daily_for_related = 23
    count_daily_self = 24
    count_top_gg_vote = 25
    daily_can_claim_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    daily_reminded = True
    entry_id = 1021
    streak = 27
    top_gg_voted_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    user_id = 202412070007
    relationship_value = 28
    relationship_divorces = 29
    relationship_slots = 30
    
    try:
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
        
        user_balance = UserBalance.from_entry(entry)
        _assert_fields_set(user_balance)
        
        # Should auto store in cache
        vampytest.assert_is(USER_BALANCE_CACHE.get(user_id, None), user_balance)
        
        vampytest.assert_eq(user_balance.allocated, allocated)
        vampytest.assert_eq(user_balance.balance, balance)
        vampytest.assert_eq(user_balance.count_daily_by_related, count_daily_by_related)
        vampytest.assert_eq(user_balance.count_daily_for_related, count_daily_for_related)
        vampytest.assert_eq(user_balance.count_daily_self, count_daily_self)
        vampytest.assert_eq(user_balance.count_top_gg_vote, count_top_gg_vote)
        vampytest.assert_eq(user_balance.daily_can_claim_at, daily_can_claim_at)
        vampytest.assert_eq(user_balance.daily_reminded, daily_reminded)
        vampytest.assert_eq(user_balance.entry_id, entry_id)
        vampytest.assert_eq(user_balance.streak, streak)
        vampytest.assert_eq(user_balance.top_gg_voted_at, top_gg_voted_at)
        vampytest.assert_eq(user_balance.user_id, user_id)
        vampytest.assert_eq(user_balance.relationship_value, relationship_value)
        vampytest.assert_eq(user_balance.relationship_divorces, relationship_divorces)
        vampytest.assert_eq(user_balance.relationship_slots, relationship_slots)
    
    finally:
        USER_BALANCE_CACHE.clear()


def test__UserBalance__from_entry__cache():
    """
    Tests whether ``UserBalance.from_entry`` works as intended.
    
    Case: Caching.
    """
    allocated = 40
    balance = 41
    count_daily_by_related = 42
    count_daily_for_related = 43
    count_daily_self = 44
    count_top_gg_vote = 45
    daily_can_claim_at = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    daily_reminded = True
    entry_id = 1022
    streak = 46
    top_gg_voted_at = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    user_id = 202412070009
    relationship_value = 47
    relationship_divorces = 48
    relationship_slots = 49
    
    try:
        user_balance = UserBalance(user_id)
        user_balance.entry_id = entry_id
        USER_BALANCE_CACHE[user_id] = user_balance
        
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
        
        output = UserBalance.from_entry(entry)
        vampytest.assert_is(output, user_balance)
        
        vampytest.assert_eq(user_balance.allocated, allocated)
        vampytest.assert_eq(user_balance.balance, balance)
        vampytest.assert_eq(user_balance.count_daily_by_related, count_daily_by_related)
        vampytest.assert_eq(user_balance.count_daily_for_related, count_daily_for_related)
        vampytest.assert_eq(user_balance.count_daily_self, count_daily_self)
        vampytest.assert_eq(user_balance.count_top_gg_vote, count_top_gg_vote)
        vampytest.assert_eq(user_balance.daily_can_claim_at, daily_can_claim_at)
        vampytest.assert_eq(user_balance.daily_reminded, daily_reminded)
        vampytest.assert_eq(user_balance.entry_id, entry_id)
        vampytest.assert_eq(user_balance.streak, streak)
        vampytest.assert_eq(user_balance.top_gg_voted_at, top_gg_voted_at)
        vampytest.assert_eq(user_balance.user_id, user_id)
        vampytest.assert_eq(user_balance.relationship_value, relationship_value)
        vampytest.assert_eq(user_balance.relationship_divorces, relationship_divorces)
        vampytest.assert_eq(user_balance.relationship_slots, relationship_slots)
    
    finally:
        USER_BALANCE_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserBalance__delete():
    """
    Tests whether ``UserBalance.delete`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202412070012
    entry_id = 1030
    
    try:
        user_balance = UserBalance(user_id)
        user_balance.entry_id = entry_id
        USER_BALANCE_CACHE[user_id] = user_balance
        
        vampytest.assert_is(user_balance.saver, None)
        vampytest.assert_is_not(USER_BALANCE_CACHE.get(user_id, None), None)
        
        user_balance.delete()
        
        vampytest.assert_is_not(user_balance.saver, None)
        vampytest.assert_is(USER_BALANCE_CACHE.get(user_id, None), None)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(user_balance.saver, None)
        vampytest.assert_is(USER_BALANCE_CACHE.get(user_id, None), None)
    
    finally:
        USER_BALANCE_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserBalance__set__add_field():
    """
    Tests whether ``UserBalance.set`` works as intended.
    
    This function is a coroutine.
    
    Case: Add field.
    """
    user_id = 202412070013
    old_relationship_value = 50
    
    new_relationship_value = 20
    
    try:
        user_balance = UserBalance(user_id)
        user_balance.relationship_value = old_relationship_value
        
        vampytest.assert_is(user_balance.saver, None)
        vampytest.assert_is(USER_BALANCE_CACHE.get(user_id, None), None)
        vampytest.assert_eq(user_balance.relationship_value, old_relationship_value)
        
        user_balance.set('relationship_value', new_relationship_value)
        
        vampytest.assert_eq(user_balance.relationship_value, new_relationship_value)
        vampytest.assert_is_not(user_balance.saver, None)
        vampytest.assert_eq(user_balance.saver.modified_fields, {'relationship_value': new_relationship_value})
        vampytest.assert_is(USER_BALANCE_CACHE.get(user_id, None), user_balance)
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_eq(user_balance.relationship_value, new_relationship_value)
        vampytest.assert_is(user_balance.saver, None)
        vampytest.assert_is(USER_BALANCE_CACHE.get(user_id, None), user_balance)
        
    finally:
        USER_BALANCE_CACHE.clear()


@vampytest.skip_if(DB_ENGINE is not None)
async def test__UserBalance__set__save():
    """
    Tests whether ``UserBalance.save`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202412070014
    
    try:
        user_balance = UserBalance(user_id)
        
        task = Task(get_event_loop(), user_balance.save())
        
        await skip_ready_cycle()
        
        vampytest.assert_is_not(user_balance.saver, None)
        
        task.apply_timeout(0.1)
        await task
        
        key = next(iter(USER_BALANCE_CACHE.keys()), None)
        vampytest.assert_is_not(key, None)
        vampytest.assert_eq(user_balance.user_id, key)
        vampytest.assert_is(USER_BALANCE_CACHE.get(key, None), user_balance)
        
        vampytest.assert_is(user_balance.saver, None)
        
    finally:
        USER_BALANCE_CACHE.clear()
