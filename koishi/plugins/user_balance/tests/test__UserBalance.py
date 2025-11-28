from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import DATETIME_FORMAT_CODE

from ..constants import USER_BALANCE_CACHE
from ..user_balance import UserBalance


def _assert_fields_set(user_balance):
    """
    Asserts whether every fields are set of the user balance.
    
    Parameters
    ----------
    user_balance : ``UserBalance``
        The user balance to test.
    """
    vampytest.assert_instance(user_balance, UserBalance)
    vampytest.assert_instance(user_balance.allocations, bytes, nullable = True)
    vampytest.assert_instance(user_balance.count_daily_by_related, int)
    vampytest.assert_instance(user_balance.count_daily_for_related, int)
    vampytest.assert_instance(user_balance.count_daily_self, int)
    vampytest.assert_instance(user_balance.count_top_gg_vote, int)
    vampytest.assert_instance(user_balance.daily_can_claim_at, DateTime)
    vampytest.assert_instance(user_balance.daily_reminded, bool)
    vampytest.assert_instance(user_balance.entry_id, int)
    vampytest.assert_instance(user_balance.relationship_value, int)
    vampytest.assert_instance(user_balance.relationship_divorces, int)
    vampytest.assert_instance(user_balance.relationship_slots, int)
    vampytest.assert_instance(user_balance.streak, int)
    vampytest.assert_instance(user_balance.top_gg_voted_at, DateTime)
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
    allocations = b'\x00' * 18
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
        user_balance.allocations = allocations
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
        vampytest.assert_in(f'allocations = {allocations!r}', output)
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


def test__UserBalance__from_entry():
    """
    Tests whether ``UserBalance.from_entry`` works as intended.
    """
    allocations = b'\x00' * 18
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
    
    entry = {
        'allocations': allocations,
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
    
    # Should not auto store in cache
    vampytest.assert_is(USER_BALANCE_CACHE.get(user_id, None), None)
    
    vampytest.assert_eq(user_balance.allocations, allocations)
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


def test__UserBalance__add_allocation__new():
    """
    Tests whether ``UserBalance.add_allocation`` works as intended.
    
    Case: new.
    """
    allocation_0 = (
        6666,
        1233,
        50,
    )
    
    user_balance = UserBalance(202511200000)
    user_balance.add_allocation(*allocation_0)
    vampytest.assert_eq(
        [*user_balance.iter_allocations()],
        [
            allocation_0,
        ],
    )
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'allocations': user_balance.allocations,
        },
    )


def test__UserBalance__add_allocation__existing():
    """
    Tests whether ``UserBalance.add_allocation`` works as intended.
    
    Case: existing.
    """
    allocation_0 = (
        6666,
        1233,
        50,
    )
    
    allocation_1 = (
        6668,
        1236,
        56,
    )
    
    user_balance = UserBalance(202511200001)
    user_balance.add_allocation(*allocation_0)
    user_balance.add_allocation(*allocation_1)
    vampytest.assert_eq(
        [*user_balance.iter_allocations()],
        [
            allocation_0,
            allocation_1,
        ],
    )
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'allocations': user_balance.allocations,
        },
    )


def test__UserBalance__get_cumulative_allocated_balance__empty():
    """
    Tests whether ``UserBalance.get_cumulative_allocated_balance`` works as intended.
    
    Case: empty.
    """
    user_balance = UserBalance(202511200002)
    
    output = user_balance.get_cumulative_allocated_balance()
    vampytest.assert_eq(output, 0)


def test__UserBalance__get_cumulative_allocated_balance__filled():
    """
    Tests whether ``UserBalance.get_cumulative_allocated_balance`` works as intended.
    
    Case: filled.
    """
    allocation_0 = (
        6666,
        1233,
        50,
    )
    
    allocation_1 = (
        6668,
        1236,
        56,
    )
    
    user_balance = UserBalance(202511200003)
    user_balance.add_allocation(*allocation_0)
    user_balance.add_allocation(*allocation_1)
    output = user_balance.get_cumulative_allocated_balance()
    vampytest.assert_eq(output, allocation_0[2] + allocation_1[2])


def test__UserBalance__remove_allocation__none():
    """
    Tests whether ``UserBalance.remove_allocation`` works as intended.
    
    Case: none.
    """
    allocation_0 = (
        6666,
        1233,
        50,
    )
    
    user_balance = UserBalance(202511200004)
    user_balance.remove_allocation(allocation_0[0], allocation_0[1])
    vampytest.assert_eq(
        [*user_balance.iter_allocations()],
        [],
    )
    vampytest.assert_eq(
        user_balance.modified_fields,
        None,
    )


def test__UserBalance__remove_allocation__existing():
    """
    Tests whether ``UserBalance.remove_allocation`` works as intended.
    
    Case: existing.
    """
    allocation_0 = (
        6666,
        1233,
        50,
    )
    
    allocation_1 = (
        6668,
        1236,
        56,
    )
    
    allocation_2 = (
        6678,
        1266,
        59,
    )
    
    user_balance = UserBalance(202511200005)
    user_balance.add_allocation(*allocation_0)
    user_balance.add_allocation(*allocation_1)
    user_balance.add_allocation(*allocation_2)
    user_balance.remove_allocation(allocation_1[0], allocation_1[1])
    vampytest.assert_eq(
        [*user_balance.iter_allocations()],
        [
            allocation_0,
            allocation_2,
        ],
    )
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'allocations': user_balance.allocations,
        },
    )


def test__UserBalance__modify_balance_by():
    """
    Tests whether ``UserBalance.modify_balance_by`` works as intended.
    """
    current = 56
    amount = -2
    
    user_balance = UserBalance(202511200006)
    user_balance.balance = current
    user_balance.modify_balance_by(amount)
    
    vampytest.assert_eq(user_balance.balance, current + amount)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'balance': user_balance.balance,
        },
    )


def test__UserBalance__modify_relationship_value_by():
    """
    Tests whether ``UserBalance.modify_relationship_value_by`` works as intended.
    """
    current = 56
    amount = -2
    
    user_balance = UserBalance(202511200007)
    user_balance.relationship_value = current
    user_balance.modify_relationship_value_by(amount)
    
    vampytest.assert_eq(user_balance.relationship_value, current + amount)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'relationship_value': user_balance.relationship_value,
        },
    )


def test__UserBalance__set_relationship_value():
    """
    Tests whether ``UserBalance.set_relationship_value`` works as intended.
    """
    current = 56
    amount = 23
    
    user_balance = UserBalance(202511200008)
    user_balance.relationship_value = current
    user_balance.set_relationship_value(amount)
    
    vampytest.assert_eq(user_balance.relationship_value, amount)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'relationship_value': user_balance.relationship_value,
        },
    )


def test__UserBalance__set_streak():
    """
    Tests whether ``UserBalance.set_streak`` works as intended.
    """
    current = 56
    amount = 23
    
    user_balance = UserBalance(202511200009)
    user_balance.streak = current
    user_balance.set_streak(amount)
    
    vampytest.assert_eq(user_balance.streak, amount)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'streak': user_balance.streak,
        },
    )


def test__UserBalance__set_daily_can_claim_at():
    """
    Tests whether ``UserBalance.set_daily_can_claim_at`` works as intended.
    """
    current = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    amount = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    user_balance = UserBalance(202511200010)
    user_balance.daily_can_claim_at = current
    user_balance.set_daily_can_claim_at(amount)
    
    vampytest.assert_eq(user_balance.daily_can_claim_at, amount)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'daily_can_claim_at': user_balance.daily_can_claim_at,
        },
    )


def test__UserBalance__set_top_gg_voted_at():
    """
    Tests whether ``UserBalance.set_top_gg_voted_at`` works as intended.
    """
    current = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    amount = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    user_balance = UserBalance(202511200011)
    user_balance.top_gg_voted_at = current
    user_balance.set_top_gg_voted_at(amount)
    
    vampytest.assert_eq(user_balance.top_gg_voted_at, amount)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'top_gg_voted_at': user_balance.top_gg_voted_at,
        },
    )


def test__UserBalance__increment_count_daily_self():
    """
    Tests whether ``UserBalance.increment_count_daily_self`` works as intended.
    """
    current = 56
    
    user_balance = UserBalance(202511200012)
    user_balance.count_daily_self = current
    user_balance.increment_count_daily_self()
    
    vampytest.assert_eq(user_balance.count_daily_self, current + 1)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'count_daily_self': user_balance.count_daily_self,
        },
    )


def test__UserBalance__increment_count_daily_for_related():
    """
    Tests whether ``UserBalance.increment_count_daily_for_related`` works as intended.
    """
    current = 56
    
    user_balance = UserBalance(202511200013)
    user_balance.count_daily_for_related = current
    user_balance.increment_count_daily_for_related()
    
    vampytest.assert_eq(user_balance.count_daily_for_related, current + 1)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'count_daily_for_related': user_balance.count_daily_for_related,
        },
    )


def test__UserBalance__increment_count_daily_by_related():
    """
    Tests whether ``UserBalance.increment_count_daily_by_related`` works as intended.
    """
    current = 56
    
    user_balance = UserBalance(202511200014)
    user_balance.count_daily_by_related = current
    user_balance.increment_count_daily_by_related()
    
    vampytest.assert_eq(user_balance.count_daily_by_related, current + 1)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'count_daily_by_related': user_balance.count_daily_by_related,
        },
    )


def test__UserBalance__increment_count_top_gg_vote():
    """
    Tests whether ``UserBalance.increment_count_top_gg_vote`` works as intended.
    """
    current = 56
    
    user_balance = UserBalance(202511200015)
    user_balance.count_top_gg_vote = current
    user_balance.increment_count_top_gg_vote()
    
    vampytest.assert_eq(user_balance.count_top_gg_vote, current + 1)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'count_top_gg_vote': user_balance.count_top_gg_vote,
        },
    )


def test__UserBalance__increment_relationship_slots():
    """
    Tests whether ``UserBalance.increment_relationship_slots`` works as intended.
    """
    current = 56
    
    user_balance = UserBalance(202511200016)
    user_balance.relationship_slots = current
    user_balance.increment_relationship_slots()
    
    vampytest.assert_eq(user_balance.relationship_slots, current + 1)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'relationship_slots': user_balance.relationship_slots,
        },
    )


def test__UserBalance__increment_relationship_divorces():
    """
    Tests whether ``UserBalance.increment_relationship_divorces`` works as intended.
    """
    current = 56
    
    user_balance = UserBalance(202511200016)
    user_balance.relationship_divorces = current
    user_balance.increment_relationship_divorces()
    
    vampytest.assert_eq(user_balance.relationship_divorces, current + 1)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'relationship_divorces': user_balance.relationship_divorces,
        },
    )


def test__UserBalance__decrement_relationship_divorces():
    """
    Tests whether ``UserBalance.decrement_relationship_divorces`` works as intended.
    """
    current = 56
    
    user_balance = UserBalance(202511200017)
    user_balance.relationship_divorces = current
    user_balance.decrement_relationship_divorces()
    
    vampytest.assert_eq(user_balance.relationship_divorces, current - 1)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'relationship_divorces': user_balance.relationship_divorces,
        },
    )


def test__UserBalance__set_daily_reminded():
    """
    Tests whether ``UserBalance.set_daily_reminded`` works as intended.
    """
    current = True
    value = False
    
    user_balance = UserBalance(202511200018)
    user_balance.daily_reminded = current
    user_balance.set_daily_reminded(value)
    
    vampytest.assert_eq(user_balance.daily_reminded, value)
    
    vampytest.assert_eq(
        user_balance.modified_fields,
        {
            'daily_reminded': user_balance.daily_reminded,
        },
    )
