from datetime import datetime as DateTime, timezone as TimeZone, timedelta as TimeDelta

import vampytest

from ...user_balance import UserBalance

from ..constants import RELATIONSHIP_CACHE_LISTING
from ..relationship import Relationship
from ..relationship_deepening import deepen_and_boost_relationship
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


async def test__deepen_and_boost_relationship__self():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: boosting self.
    """
    source_user_id = 202503070004
    
    source_user_balance = UserBalance(source_user_id)
    
    await deepen_and_boost_relationship(source_user_balance, None, None, 1000)
    
    vampytest.assert_eq(source_user_balance.balance, 0)
    vampytest.assert_eq(source_user_balance.relationship_value, 10)


async def test__deepen_and_boost_relationship__other():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: Boosting other.
    """
    source_user_id = 202503070005
    target_user_id = 202503070006
    
    
    source_user_balance = UserBalance(source_user_id)
    target_user_balance = UserBalance(target_user_id)
    
    await deepen_and_boost_relationship(source_user_balance, target_user_balance, None, 1000)
    
    vampytest.assert_eq(source_user_balance.balance, 0)
    vampytest.assert_eq(source_user_balance.relationship_value, 5)
    
    vampytest.assert_eq(target_user_balance.balance, 0)
    vampytest.assert_eq(target_user_balance.relationship_value, 0)


async def test__deepen_and_boost_relationship__direct_related_without_boost():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: Direct related without boost.
    """
    source_user_id = 202503070007
    target_user_id = 202503070008
    
    now = DateTime.now(TimeZone.utc) + TimeDelta(days = 300)
    
    source_user_balance = UserBalance(source_user_id)
    target_user_balance = UserBalance(target_user_id)
    
    relationship_to_deepen = Relationship(source_user_id, target_user_id, RELATIONSHIP_TYPE_MAMA, 0, now)
    
    try:
        await deepen_and_boost_relationship(source_user_balance, target_user_balance, relationship_to_deepen, 1000)
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
    
    vampytest.assert_eq(source_user_balance.balance, 0)
    vampytest.assert_eq(source_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(target_user_balance.balance, 0)
    vampytest.assert_eq(target_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(relationship_to_deepen.source_investment, 10)
    vampytest.assert_eq(relationship_to_deepen.source_can_boost_at, now)
    vampytest.assert_eq(relationship_to_deepen.target_investment, 0)
    vampytest.assert_eq(relationship_to_deepen.target_can_boost_at, now)


async def test__deepen_and_boost_relationship__indirect_related_without_boost():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: Indirect related without boost.
    """
    source_user_id = 202503070009
    target_user_id = 202503070010
    middle_user_id = 202503070011
    
    now = DateTime.now(TimeZone.utc) + TimeDelta(days = 300)
    
    source_user_balance = UserBalance(source_user_id)
    target_user_balance = UserBalance(target_user_id)
    
    relationship_to_deepen = Relationship(source_user_id, middle_user_id, RELATIONSHIP_TYPE_MAMA, 0, now)
    
    try:
        await deepen_and_boost_relationship(source_user_balance, target_user_balance, relationship_to_deepen, 1000)
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
    
    vampytest.assert_eq(source_user_balance.balance, 0)
    vampytest.assert_eq(source_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(target_user_balance.balance, 0)
    vampytest.assert_eq(target_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(relationship_to_deepen.source_investment, 5)
    vampytest.assert_eq(relationship_to_deepen.source_can_boost_at, now)
    vampytest.assert_eq(relationship_to_deepen.target_investment, 0)
    vampytest.assert_eq(relationship_to_deepen.target_can_boost_at, now)


async def test__deepen_and_boost_relationship__direct_related_with_boost():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: Direct related with boost.
    """
    source_user_id = 202503070012
    target_user_id = 202503070013
    
    now = DateTime.now(TimeZone.utc) - TimeDelta(days = 300)
    
    source_user_balance = UserBalance(source_user_id)
    target_user_balance = UserBalance(target_user_id)
    
    relationship_to_deepen = Relationship(source_user_id, target_user_id, RELATIONSHIP_TYPE_MAMA, 0, now)
    
    try:
        await deepen_and_boost_relationship(source_user_balance, target_user_balance, relationship_to_deepen, 1000)
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
    
    vampytest.assert_eq(source_user_balance.balance, 50)
    vampytest.assert_eq(source_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(target_user_balance.balance, 25)
    vampytest.assert_eq(target_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(relationship_to_deepen.source_investment, 10)
    vampytest.assert_ne(relationship_to_deepen.source_can_boost_at, now)
    vampytest.assert_eq(relationship_to_deepen.target_investment, 0)
    vampytest.assert_eq(relationship_to_deepen.target_can_boost_at, now)


async def test__deepen_and_boost_relationship__inverted_direct_related_with_boost():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: Inverted direct related with boost.
    """
    source_user_id = 202503070020
    target_user_id = 202503070021
    
    now = DateTime.now(TimeZone.utc) - TimeDelta(days = 300)
    
    source_user_balance = UserBalance(source_user_id)
    target_user_balance = UserBalance(target_user_id)
    
    relationship_to_deepen = Relationship(target_user_id, source_user_id, RELATIONSHIP_TYPE_MAMA, 0, now)
    
    try:
        await deepen_and_boost_relationship(source_user_balance, target_user_balance, relationship_to_deepen, 1000)
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
    
    vampytest.assert_eq(source_user_balance.balance, 50)
    vampytest.assert_eq(source_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(target_user_balance.balance, 25)
    vampytest.assert_eq(target_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(relationship_to_deepen.source_investment, 0)
    vampytest.assert_eq(relationship_to_deepen.source_can_boost_at, now)
    vampytest.assert_eq(relationship_to_deepen.target_investment, 10)
    vampytest.assert_ne(relationship_to_deepen.target_can_boost_at, now)


async def test__deepen_and_boost_relationship__indirect_related_with_boost():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: indirect related with boost.
    """
    source_user_id = 202503070014
    target_user_id = 202503070015
    middle_user_id = 202503070016
    
    now = DateTime.now(TimeZone.utc) - TimeDelta(days = 300)
    
    source_user_balance = UserBalance(source_user_id)
    target_user_balance = UserBalance(target_user_id)
    
    relationship_to_deepen = Relationship(source_user_id, middle_user_id, RELATIONSHIP_TYPE_MAMA, 0, now)
    
    try:
        await deepen_and_boost_relationship(source_user_balance, target_user_balance, relationship_to_deepen, 1000)
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
    
    vampytest.assert_eq(source_user_balance.balance, 25)
    vampytest.assert_eq(source_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(target_user_balance.balance, 12)
    vampytest.assert_eq(target_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(relationship_to_deepen.source_investment, 5)
    vampytest.assert_ne(relationship_to_deepen.source_can_boost_at, now)
    vampytest.assert_eq(relationship_to_deepen.target_investment, 0)
    vampytest.assert_eq(relationship_to_deepen.target_can_boost_at, now)


async def test__deepen_and_boost_relationship__inverted_indirect_related_with_boost():
    """
    Tests whether ``deepen_and_boost_relationship`` works as intended.
    
    Case: inverted indirect related with boost.
    """
    source_user_id = 202503070017
    target_user_id = 202503070018
    middle_user_id = 202503070019
    
    now = DateTime.now(TimeZone.utc) - TimeDelta(days = 300)
    
    source_user_balance = UserBalance(source_user_id)
    target_user_balance = UserBalance(target_user_id)
    
    relationship_to_deepen = Relationship(middle_user_id, source_user_id, RELATIONSHIP_TYPE_MAMA, 0, now)
    
    try:
        await deepen_and_boost_relationship(source_user_balance, target_user_balance, relationship_to_deepen, 1000)
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
    
    vampytest.assert_eq(source_user_balance.balance, 25)
    vampytest.assert_eq(source_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(target_user_balance.balance, 12)
    vampytest.assert_eq(target_user_balance.relationship_value, 0)
    
    vampytest.assert_eq(relationship_to_deepen.source_investment, 0)
    vampytest.assert_eq(relationship_to_deepen.source_can_boost_at, now)
    vampytest.assert_eq(relationship_to_deepen.target_investment, 5)
    vampytest.assert_ne(relationship_to_deepen.target_can_boost_at, now)
