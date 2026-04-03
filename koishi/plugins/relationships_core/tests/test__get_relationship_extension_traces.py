from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..constants import RELATIONSHIP_LISTING_CACHE
from ..relationship import Relationship
from ..relationship_extension_trace import RelationshipExtensionTrace
from ..relationship_queries import get_relationship_extension_traces
from ..relationship_types import (
    RELATIONSHIP_TYPE_AUNTIE, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP,
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP,
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_STEP, RELATIONSHIP_TYPE_CO_WORKER, RELATIONSHIP_TYPE_DAUGHTER,
    RELATIONSHIP_TYPE_GRANDDAUGHTER, RELATIONSHIP_TYPE_GRANNY, RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_MAMA,
    RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_NANNY, RELATIONSHIP_TYPE_NIECE, RELATIONSHIP_TYPE_SISTER_BIG,
    RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_TEA_FRIEND, RELATIONSHIP_TYPE_UNSET, RELATIONSHIP_TYPE_WAIFU,
    RELATIONSHIP_TYPE_YOUNG_MISTRESS
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
        'nothing',
        (
            (
                user_id_00,
                None,
            ),
        ),
        user_id_00,
        None,
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
        'waifu',
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
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_0,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_SISTER_BIG | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_1),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_SISTER_LIL | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_2),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_MAMA | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_3),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_DAUGHTER | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_4),
            ),
            user_id_07 : RelationshipExtensionTrace(
                user_id_07,
                RELATIONSHIP_TYPE_MAID | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP),
                (relationship_0, relationship_6),
            ),
        },
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
        'big sister',
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
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_SISTER_BIG,
                (relationship_0,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_SISTER_BIG | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_1),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_SISTER_BIG | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_2),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_SISTER_LIL | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_3),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_MAMA | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_STEP << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_4),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_NIECE,
                (relationship_0, relationship_5),
            ),
        },
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
        'big sis',
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
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_SISTER_LIL,
                (relationship_0,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_SISTER_LIL | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_1),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_SISTER_LIL | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_2),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_SISTER_LIL | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_3),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_MAMA | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_STEP << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_4),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_NIECE,
                (relationship_0, relationship_5),
            ),
        },
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
        'mama',
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
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_0,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MAMA | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_1),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_AUNTIE,
                (relationship_0, relationship_2),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_AUNTIE,
                (relationship_0, relationship_3),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_GRANNY,
                (relationship_0, relationship_4),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_SISTER_LIL | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_SISTERSHIP),
                (relationship_0, relationship_5),
            ),
            user_id_08 : RelationshipExtensionTrace(
                user_id_08,
                RELATIONSHIP_TYPE_NANNY,
                (relationship_0, relationship_7),
            ),
        }
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
        'daughter',
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
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_0,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_DAUGHTER | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_1),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_DAUGHTER | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_2),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_DAUGHTER | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_HALF << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_0, relationship_3),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_GRANDDAUGHTER,
                (relationship_0, relationship_5),
            ),
            user_id_07 : RelationshipExtensionTrace(
                user_id_07,
                RELATIONSHIP_TYPE_TEA_FRIEND,
                (relationship_0, relationship_6),
            ),
        },
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
        'mistress',
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
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_MISTRESS,
                (relationship_0,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MISTRESS | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_EMPLOYMENTSHIP),
                (relationship_0, relationship_1),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_YOUNG_MISTRESS,
                (relationship_0, relationship_5),
            ),
            user_id_08 : RelationshipExtensionTrace(
                user_id_08,
                RELATIONSHIP_TYPE_CO_WORKER,
                (relationship_0, relationship_7),
            ),
        },
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
        'maid',
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
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_MAID,
                (relationship_0,),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_TEA_FRIEND,
                (relationship_0, relationship_4),
            ),
        },
    )
    
    relationship_0 = Relationship(user_id_00, user_id_01, RELATIONSHIP_TYPE_UNSET, 1203, now)
    
    yield (
        'unset',
        (
            (
                user_id_00,
                (
                    relationship_0,
                ),
            ),
        ),
        user_id_00,
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_UNSET,
                (relationship_0,),
            ),
        },
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
async def test__get_relationship_extension_traces__in_cache(cache, user_id):
    """
    Tests whether ``get_relationship_extension_traces`` works as intended.
    
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
    output : ``None | dict<int, RelationshipExtensionTrace>``
    """
    async def mock_query_relationship_listing(input_user_id):
        raise RuntimeError
    
    async def mock_query_relationship_listings(input_user_ids):
        raise RuntimeError
    
    mocked = vampytest.mock_globals(
        get_relationship_extension_traces,
        3,
        query_relationship_listing = mock_query_relationship_listing,
        query_relationship_listings = mock_query_relationship_listings,
    )
    
    try:
        for cache_user_id, cache_relationships in cache:
            RELATIONSHIP_LISTING_CACHE[cache_user_id] = None if cache_relationships is None else [*cache_relationships]
        
        output = await mocked(user_id)
        
    finally:
        RELATIONSHIP_LISTING_CACHE.clear()
        
    vampytest.assert_instance(output, dict, nullable = True)
    return output
