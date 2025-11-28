from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import User

from ...relationships_core import RELATIONSHIP_TYPE_SISTER_LIL, Relationship
from ...user_balance import UserBalance

from ..related_completion import get_related_users_with_name_and_next_daily


def _iter_options():
    user_id_0 = 202412110008_000000
    guild_id = 202412110011_000000
    user_id_1 = 202412110009_000000
    user_id_2 = 202412110010_000000
    
    related_daily_can_claim_at_1 = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    related_daily_can_claim_at_2 = DateTime(2016, 5, 15, tzinfo = TimeZone.utc)
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    relationship_1 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    
    user_1 = User.precreate(user_id_1, name = 'koishi')
    user_2 = User.precreate(user_id_2, name = 'remilia')
    
    user_balance_1 = UserBalance(user_id_1)
    user_balance_1.set_daily_can_claim_at(related_daily_can_claim_at_1)
    
    user_balance_2 = UserBalance(user_id_2)
    user_balance_2.set_daily_can_claim_at(related_daily_can_claim_at_2)
    
    
    yield (
        [
            relationship_0,
            relationship_1,
        ],
        [
            user_balance_2,
        ],
        [
            user_1,
            user_2,
        ],
        user_id_0,
        'remilia',
        guild_id,
        {
            user_2: related_daily_can_claim_at_2,
        },
    )
    
    yield (
        [
            relationship_0,
            relationship_1,
        ],
        [
            user_balance_1,
        ],
        [
            user_1,
            user_2,
        ],
        user_id_0,
        str(user_id_1),
        guild_id,
        {
            user_1: related_daily_can_claim_at_1,
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_related_users_with_name_and_next_daily(relationships, user_balances, users, user_id, name, guild_id):
    """
    Tests whether ``get_related_users_with_name_and_next_daily`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    relationship : `None | list<(Relationship, None | list<Relationship>)>`
        Relationships of the user.
    
    user_balances : `list<UserBalance>`
        User balances of the filtered users.
    
    users : `list<ClientUserBase>`
        Users mentioned in the relationships. Excluding the source user obviously.
    
    user_id : `int`
        Use id to query for.
    
    guild_id : `int`
        Respective guild's identifier to extend matching for.
    
    value : `None | str`
        Value to match.
    
    Returns
    -------
    output : `dict<ClientUserBase, DateTime>`
    """
    async def mock_get_relationship_listing_with_extend(input_user_id):
        nonlocal user_id
        nonlocal relationships
        
        vampytest.assert_eq(user_id, input_user_id)
        
        return [(relationship, None) for relationship in relationships]
    
    
    async def mock_get_user_balances(input_user_ids):
        nonlocal user_balances
        
        vampytest.assert_eq({*input_user_ids}, {user_balance.user_id for user_balance in user_balances})
        
        return {
            user_balance.user_id: user_balance for user_balance in user_balances
        }
    
    
    async def mock_get_users_unordered(input_user_ids):
        nonlocal users
        
        vampytest.assert_eq({*input_user_ids}, {user.id for user in users})
        
        return users
    
    mocked = vampytest.mock_globals(
        get_related_users_with_name_and_next_daily,
        get_relationship_listing_with_extend = mock_get_relationship_listing_with_extend,
        get_user_balances = mock_get_user_balances,
        get_users_unordered = mock_get_users_unordered,
    )
    
    output = await mocked(user_id, guild_id, name)
    vampytest.assert_instance(output, dict)
    return output
