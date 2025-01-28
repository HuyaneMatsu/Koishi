from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import RELATIONSHIP_CACHE_LISTING
from ..relationship import Relationship
from ..relationship_queries import get_relationship_listing_and_extend
from ..relationship_types import (
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_UNSET,
    RELATIONSHIP_TYPE_WAIFU
)


def _iter_options():
    user_id_00 = 202501040060
    user_id_01 = 202501040061
    user_id_02 = 202501040062
    user_id_03 = 202501040063
    user_id_04 = 202501040064
    user_id_05 = 202501040065
    user_id_06 = 202501040066
    user_id_07 = 202501040067
    user_id_08 = 202501040068
    user_id_09 = 202501040069
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    # Nothing
    yield (
        (
            (
                user_id_00,
                None,
            ),
        ),
        user_id_00,
        (
            None,
            None,
        )
    )
    
    # Sharing through waifu
    
    relationship_0 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    relationship_1 = Relationship(user_id_02, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_2 = Relationship(user_id_01, user_id_03, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_3 = Relationship(user_id_04, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_4 = Relationship(user_id_01, user_id_05, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_5 = Relationship(user_id_06, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_6 = Relationship(user_id_01, user_id_07, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    
    # Extras:
    relationship_7 = Relationship(user_id_01, user_id_08, RELATIONSHIP_TYPE_UNSET, 1203, now)
    relationship_8 = Relationship(user_id_01, user_id_09, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ), (
                user_id_01,
                (
                    relationship_1,
                    relationship_2,
                    relationship_3,
                    relationship_4,
                    relationship_5,
                    relationship_6,
                    
                    # Extras:
                    relationship_7,
                    relationship_8,
                )
            )
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            [
                (
                    relationship_0,
                    [
                        relationship_1,
                        relationship_2,
                        relationship_3,
                        relationship_4,
                        # do not add mistress
                        relationship_6,
                        
                        # extras:
                        # do not add unset
                        # do not add waifu
                    ],
                )
            ],
        )
    )
    
    # Sharing through big sister
    
    relationship_0 = Relationship(user_id_01, user_id_00, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_1 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    relationship_2 = Relationship(user_id_03, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_3 = Relationship(user_id_01, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_4 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_5 = Relationship(user_id_01, user_id_06, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_6 = Relationship(user_id_07, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_7 = Relationship(user_id_01, user_id_08, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    
    # Extras:
    relationship_8 = Relationship(user_id_01, user_id_09, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ), (
                user_id_01,
                (
                    relationship_1,
                    relationship_2,
                    relationship_3,
                    relationship_4,
                    relationship_5,
                    relationship_6,
                    relationship_7,
                    
                    # Extras:
                    relationship_8,
                )
            )
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            [
                (
                    relationship_0,
                    [
                        relationship_1,
                        # TBD,
                        # TBD,
                        # TBD,
                        # TBD
                        # TBD
                        
                        # extras:
                        # do not add unset
                    ],
                )
            ],
        )
    )
    
    
    # Sharing through lil sister
    
    relationship_0 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_1 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    relationship_2 = Relationship(user_id_03, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_3 = Relationship(user_id_01, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_4 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_5 = Relationship(user_id_01, user_id_06, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_6 = Relationship(user_id_07, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_7 = Relationship(user_id_01, user_id_08, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    
    # Extras:
    relationship_8 = Relationship(user_id_01, user_id_09, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ), (
                user_id_01,
                (
                    relationship_1,
                    relationship_2,
                    relationship_3,
                    relationship_4,
                    relationship_5,
                    relationship_6,
                    relationship_7,
                    
                    # Extras:
                    relationship_8,
                )
            )
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            [
                (
                    relationship_0,
                    [
                        relationship_1,
                        # TBD,
                        # TBD,
                        # TBD,
                        # TBD
                        # TBD
                        
                        # extras:
                        # do not add unset
                    ],
                )
            ],
        )
    )
    
    
    # Sharing through mama
    
    relationship_0 = Relationship(user_id_01, user_id_00, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_1 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    relationship_2 = Relationship(user_id_03, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_3 = Relationship(user_id_01, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_4 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_5 = Relationship(user_id_01, user_id_06, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_6 = Relationship(user_id_07, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_7 = Relationship(user_id_01, user_id_08, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    
    # Extras:
    relationship_8 = Relationship(user_id_01, user_id_09, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ), (
                user_id_01,
                (
                    relationship_1,
                    relationship_2,
                    relationship_3,
                    relationship_4,
                    relationship_5,
                    relationship_6,
                    relationship_7,
                    
                    # Extras:
                    relationship_8,
                )
            )
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            [
                (
                    relationship_0,
                    [
                        relationship_1,
                        # TBD,
                        # TBD,
                        # TBD,
                        # TBD
                        # TBD
                        
                        # extras:
                        # do not add unset
                    ],
                )
            ],
        )
    )

    
    
    # Sharing through daughter
    
    relationship_0 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_1 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    relationship_2 = Relationship(user_id_03, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_3 = Relationship(user_id_01, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_4 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_5 = Relationship(user_id_01, user_id_06, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_6 = Relationship(user_id_07, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_7 = Relationship(user_id_01, user_id_08, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    
    # Extras:
    relationship_8 = Relationship(user_id_01, user_id_09, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ), (
                user_id_01,
                (
                    relationship_1,
                    relationship_2,
                    relationship_3,
                    relationship_4,
                    relationship_5,
                    relationship_6,
                    relationship_7,
                    
                    # Extras:
                    relationship_8,
                )
            )
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            [
                (
                    relationship_0,
                    [
                        relationship_1,
                        # TBD,
                        # TBD,
                        # TBD,
                        # TBD
                        # TBD
                        
                        # extras:
                        # do not add unset
                    ],
                )
            ],
        )
    )
    
    
    # Sharing through mistress
    
    relationship_0 = Relationship(user_id_01, user_id_00, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_1 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    relationship_2 = Relationship(user_id_03, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_3 = Relationship(user_id_01, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_4 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_5 = Relationship(user_id_01, user_id_06, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_6 = Relationship(user_id_07, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_7 = Relationship(user_id_01, user_id_08, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    
    # Extras:
    relationship_8 = Relationship(user_id_01, user_id_09, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ), (
                user_id_01,
                (
                    relationship_1,
                    relationship_2,
                    relationship_3,
                    relationship_4,
                    relationship_5,
                    relationship_6,
                    relationship_7,
                    
                    # Extras:
                    relationship_8,
                )
            )
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            [
                (
                    relationship_0,
                    [
                        relationship_1,
                        # TBD,
                        # TBD,
                        # TBD,
                        # TBD
                        # TBD
                        
                        # extras:
                        # do not add unset
                    ],
                )
            ],
        )
    )

    
    # Sharing through maid
    
    relationship_0 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_1 = Relationship(user_id_01, user_id_02, RELATIONSHIP_TYPE_WAIFU, 1203, now)
    relationship_2 = Relationship(user_id_03, user_id_01, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_3 = Relationship(user_id_01, user_id_04, RELATIONSHIP_TYPE_SISTER_BIG, 1203, now)
    relationship_4 = Relationship(user_id_05, user_id_01, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_5 = Relationship(user_id_01, user_id_06, RELATIONSHIP_TYPE_MAMA, 1203, now)
    relationship_6 = Relationship(user_id_07, user_id_01, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    relationship_7 = Relationship(user_id_01, user_id_08, RELATIONSHIP_TYPE_MISTRESS, 1203, now)
    
    # Extras:
    relationship_8 = Relationship(user_id_01, user_id_09, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ),
            # All is N / A or TBD
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            # all is N / A or TBD
            None,
        ),
    )

    
    # Sharing through unset (not sharing and will not share)
    
    relationship_0 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ),
        ),
        user_id_00,
        (
            [
                relationship_0
            ],
            None,
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_relationship_listing_and_extend__in_cache(cache, user_id):
    """
    Tests whether ``get_relationship_listing_and_extend`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    
    Parameters
    ----------
    cache : `tuple<(int, tuple<Relationship>)>`
        Values to populate the cache with.
    
    user_id : `int`
        User identifier to get relationship listing and extend for.
    
    Returns
    -------
    output : `(None | list<Relationship>, None | list<(Relationship, list<Relationship>)>)`
    """
    async def mock_query_relationship_listing(input_user_id, input_outgoing):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_relationship_listing_and_extend,
        query_relationship_listing = mock_query_relationship_listing,
    )
    
    try:
        for cache_user_id, cache_relationships in cache:
            RELATIONSHIP_CACHE_LISTING[cache_user_id] = None if cache_relationships is None else [*cache_relationships]
        
        output = await mocked(user_id)
        
    finally:
        RELATIONSHIP_CACHE_LISTING.clear()
        
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    relationship_listing, relationship_listing_extend = output
    vampytest.assert_instance(relationship_listing, list, nullable = True)
    vampytest.assert_instance(relationship_listing_extend, list, nullable = True)
    
    return output
