from datetime import datetime as DateTime, timezone as TimeZone


import vampytest

from ..constants import RELATIONSHIP_LISTING_CACHE
from ..relationship import Relationship
from ..relationship_queries import get_relationship_listings
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


async def test__get_relationship_listings__cached():
    """
    Tests whether ``get_relationship_listings`` works as intended.
    
    Case: cached.
    """
    source_user_id_0 = 202601200010
    target_user_id_0 = 202601200011
    source_user_id_1 = 202601200012
    target_user_id_1 = 202601200013
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(
        source_user_id_0,
        target_user_id_0,
        RELATIONSHIP_TYPE_MAMA,
        1200,
        now,
    )
    
    relationship_1 = Relationship(
        source_user_id_1,
        target_user_id_1,
        RELATIONSHIP_TYPE_MAMA,
        1203,
        now,
    )
    
    async def mocked_query_relationship_listing(user_id, waiters):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_relationship_listings,
        query_relationship_listing = mocked_query_relationship_listing,
        recursion = 2
    )
    
    
    try:
        RELATIONSHIP_LISTING_CACHE[source_user_id_0] = [relationship_0]
        RELATIONSHIP_LISTING_CACHE[source_user_id_1] = [relationship_1]
        
        vampytest.assert_eq(
            [*RELATIONSHIP_LISTING_CACHE.keys()],
            [source_user_id_0, source_user_id_1],
        )
        
        output = await mocked((source_user_id_0, source_user_id_1),)
        vampytest.assert_instance(output, dict)
        vampytest.assert_eq(
            output,
            {source_user_id_0: [relationship_0], source_user_id_1: [relationship_1]},
        )
        
        vampytest.assert_eq(
            [*RELATIONSHIP_LISTING_CACHE.items()],
            [
                (source_user_id_0, [relationship_0]),
                (source_user_id_1, [relationship_1]),
            ],
        )
    finally:
        RELATIONSHIP_LISTING_CACHE.clear()
