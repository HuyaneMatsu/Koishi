from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import User

from ...relationships_core import RELATIONSHIP_TYPE_SISTER_LIL, Relationship
from ...user_balance import UserBalance

from ..related_completion import get_related_users_with_name_and_next_daily


async def test__get_related_users_with_name_and_next_daily():
    """
    Tests whether ``get_related_users_with_name_and_next_daily`` works as intended.
    
    This function is a coroutine.
    """
    user_id = 202412110008
    name = 'remilia'
    guild_id = 202412110011
    related_id_0 = 202412110009
    related_id_1 = 202412110010
    related_daily_can_claim_at_0 = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    related_daily_can_claim_at_1 = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    related_name_0 = 'koishi'
    related_name_1 = 'remilia'
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id, related_id_0, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    relationship_1 = Relationship(user_id, related_id_1, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    
    async def mock_get_relationship_listing_with_extend(input_user_id):
        nonlocal user_id
        nonlocal relationship_0
        nonlocal relationship_1
        
        vampytest.assert_eq(user_id, input_user_id)
        return [(relationship_0, None), (relationship_1, None)]
    
    async def mock_get_user_balances(input_user_ids):
        nonlocal related_id_1
        nonlocal related_daily_can_claim_at_1
        
        vampytest.assert_eq({*input_user_ids}, {related_id_1})
        
        user_balance_1 = UserBalance(related_id_1)
        user_balance_1.set('daily_can_claim_at', related_daily_can_claim_at_1)
        
        return {
            related_id_1: user_balance_1,
        }
    
    
    async def mock_get_users_unordered(input_user_ids):
        nonlocal related_id_0
        nonlocal related_id_1
        nonlocal related_name_0
        nonlocal related_name_1
        
        vampytest.assert_eq({*input_user_ids}, {related_id_0, related_id_1})
        
        user_0 = User.precreate(related_id_0, name = related_name_0)
        user_1 = User.precreate(related_id_1, name = related_name_1)
        
        return [user_0, user_1]
    
    mocked = vampytest.mock_globals(
        get_related_users_with_name_and_next_daily,
        get_relationship_listing_with_extend = mock_get_relationship_listing_with_extend,
        get_user_balances = mock_get_user_balances,
        get_users_unordered = mock_get_users_unordered,
    )
    
    output = await mocked(user_id, guild_id, name)
    vampytest.assert_eq(
        output,
        {
            User.precreate(related_id_1): related_daily_can_claim_at_1,
        },
    )
