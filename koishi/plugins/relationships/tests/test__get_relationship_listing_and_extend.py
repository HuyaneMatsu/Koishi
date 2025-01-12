from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import RELATIONSHIP_CACHE_LISTING
from ..relationship import Relationship
from ..relationship_queries import get_relationship_listing_and_extend
from ..relationship_types import RELATIONSHIP_TYPE_MASTER, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU


async def test__get_relationship_listing_and_extend__in_cache():
    """
    Tests whether ``get_relationship_listing_and_extend`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    """
    async def mock_query_relationship_listing(input_user_id, input_outgoing):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_relationship_listing_and_extend,
        query_relationship_listing = mock_query_relationship_listing,
    )
    
    user_id_0 = 202501040060
    user_id_1 = 202501040061
    user_id_2 = 202501040062
    user_id_3 = 202501040063
    user_id_4 = 202501040064
    user_id_5 = 202501040065
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(
        user_id_1,
        user_id_0,
        RELATIONSHIP_TYPE_MASTER,
        1200,
        now,
    )
    
    relationship_1 = Relationship(
        user_id_2,
        user_id_0,
        RELATIONSHIP_TYPE_WAIFU,
        1203,
        now,
    )
    
    relationship_2 = Relationship(
        user_id_3,
        user_id_2,
        RELATIONSHIP_TYPE_MASTER,
        1203,
        now,
    )
    
    relationship_3 = Relationship(
        user_id_4,
        user_id_2,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1203,
        now,
    )
    
    relationship_4 = Relationship(
        user_id_4,
        user_id_0,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1203,
        now,
    )
    
    relationship_5 = Relationship(
        user_id_5,
        user_id_2,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1203,
        now,
    )
    
    try:
        RELATIONSHIP_CACHE_LISTING[user_id_0] = [relationship_0, relationship_1, relationship_4]
        RELATIONSHIP_CACHE_LISTING[user_id_2] = [relationship_1, relationship_2, relationship_3, relationship_5]
        
        output = await mocked(user_id_0)
        vampytest.assert_instance(output, tuple)
        vampytest.assert_eq(len(output), 2)
        relationship_listing, relationship_listing_extend = output
        vampytest.assert_instance(relationship_listing, list, nullable = True)
        vampytest.assert_eq(
            relationship_listing,
            [relationship_0, relationship_1, relationship_4],
        )
        vampytest.assert_instance(relationship_listing_extend, list, nullable = True)
        vampytest.assert_eq(
            relationship_listing_extend,
            [
                (relationship_1, [relationship_5]),
            ],
        )
        
        
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
