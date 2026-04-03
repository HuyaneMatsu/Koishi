from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import User

from ...relationships_core import (
    RELATIONSHIP_TYPE_AUNTIE, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP,
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
    RELATIONSHIP_TYPE_CO_WORKER, RELATIONSHIP_TYPE_DAUGHTER, RELATIONSHIP_TYPE_GRANDDAUGHTER, RELATIONSHIP_TYPE_MAID,
    RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_NIECE, RELATIONSHIP_TYPE_SISTER_BIG,
    RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_WAIFU, Relationship, RelationshipExtensionTrace
)

from ..relationship_listing_rendering_legacy import create_relationship_listing_pages_legacy


def _iter_options():
    user_id_00 = 202601240000
    user_id_01 = 202601240001
    user_id_02 = 202601240002
    user_id_03 = 202601240003
    user_id_04 = 202601240004
    user_id_05 = 202601240005
    user_id_06 = 202601240006
    user_id_07 = 202601240007
    user_id_08 = 202601240008
    user_id_09 = 202601240009
    user_id_10 = 202601240010
    user_id_11 = 202601240011
    user_id_12 = 202601240012
    
    user_00 = User.precreate(
        user_id_00,
        name = 'Satori',
    )
    
    user_01 = User.precreate(
        user_id_01,
        name = 'Reisen',
    )
    
    user_02 = User.precreate(
        user_id_02,
        name = 'Koishi',
    )
    
    user_03 = User.precreate(
        user_id_03,
        name = 'Momiji',
    )
    
    user_04 = User.precreate(
        user_id_04,
        name = 'Orin',
    )
    
    user_05 = User.precreate(
        user_id_05,
        name = 'Aya',
    )
    
    user_06 = User.precreate(
        user_id_06,
        name = 'Kaguya',
    )
    
    user_07 = User.precreate(
        user_id_07,
        name = 'Hatate',
    )
    
    user_08 = User.precreate(
        user_id_08,
        name = 'Keine',
    )
    
    user_09 = User.precreate(
        user_id_09,
        name = 'Keiki',
    )
    
    user_10 = User.precreate(
        user_id_10,
        name = 'Mayumi',
    )
    
    user_11 = User.precreate(
        user_id_11,
        name = 'Biten',
    )
    
    user_12 = User.precreate(
        user_id_12,
        name = 'Eirin',
    )
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        'none',
        None,
        None,
        0,
        None,
    )
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    yield (
        'single',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_00,),
           )
        },
        [
            user_01,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_MAMA,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                    ],
                ),
            ],
        ],
    )
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_MAMA | RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    yield (
        'single - one user with 2 types',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_MAMA | RELATIONSHIP_TYPE_WAIFU,
                (relationship_00,),
            ),
        },
        [
            user_01,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_WAIFU,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                    ],
                ),
            ],
        ],
    )
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    relationship_01 = Relationship(
        user_id_00,
        user_id_02,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    yield (
        'two in a single group',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_00,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_01,),
            ),
        },
        [
            user_01,
            user_02,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_MAMA,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Koishi'),
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                    ],
                ),
            ],
        ],
    )
    
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    relationship_01 = Relationship(
        user_id_01,
        user_id_02,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    yield (
        'two in a single group, with alternative',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_00,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MAMA | (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW << RELATIONSHIP_TYPE_CONNECTION_MODIFIER_SHIFT_ANCESTORSHIP),
                (relationship_00, relationship_01),
            ),
        },
        [
            user_01,
            user_02,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_MAMA,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW, 'Koishi'),
                    ],
                ),
            ],
        ],
    )
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_01 = Relationship(
        user_id_00,
        user_id_02,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    yield (
        'two in separate groups',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_00,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_01,),
            ),
        },
        [
            user_01,
            user_02,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_WAIFU,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MAMA,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Koishi'),
                    ],
                ),
            ],
        ],
    )
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_01 = Relationship(
        user_id_00,
        user_id_02,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    relationship_02 = Relationship(
        user_id_00,
        user_id_03,
        RELATIONSHIP_TYPE_SISTER_LIL,
        1000,
        now,
    )
    
    relationship_03 = Relationship(
        user_id_00,
        user_id_04,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1000,
        now,
    )
    
    relationship_04 = Relationship(
        user_id_00,
        user_id_05,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_05 = Relationship(
        user_id_00,
        user_id_06,
        RELATIONSHIP_TYPE_MISTRESS,
        1000,
        now,
    )
    
    relationship_06 = Relationship(
        user_id_00,
        user_id_07,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    relationship_07 = Relationship(
        user_id_03,
        user_id_08,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_08 = Relationship(
        user_id_02,
        user_id_09,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1000,
        now,
    )
    
    relationship_09 = Relationship(
        user_id_05,
        user_id_10,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_10 = Relationship(
        user_id_06,
        user_id_11,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    yield (
        'complex, multiple pages, regular cutoff',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_00,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_01,),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_SISTER_LIL,
                (relationship_02,),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_SISTER_BIG,
                (relationship_03,),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_04,),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_MISTRESS,
                (relationship_05,),
            ),
            user_id_07 : RelationshipExtensionTrace(
                user_id_07,
                RELATIONSHIP_TYPE_MAID,
                (relationship_06,),
            ),
            user_id_08 : RelationshipExtensionTrace(
                user_id_08,
                RELATIONSHIP_TYPE_NIECE,
                (relationship_02, relationship_07),
            ),
            user_id_09 : RelationshipExtensionTrace(
                user_id_09,
                RELATIONSHIP_TYPE_AUNTIE,
                (relationship_01, relationship_08),
            ),
            user_id_10 : RelationshipExtensionTrace(
                user_id_10,
                RELATIONSHIP_TYPE_GRANDDAUGHTER,
                (relationship_04, relationship_09),
            ),
            user_id_11 : RelationshipExtensionTrace(
                user_id_11,
                RELATIONSHIP_TYPE_CO_WORKER,
                (relationship_05, relationship_10),
            ),
        },
        [
            user_01,
            user_02,
            user_03,
            user_04,
            user_05,
            user_06,
            user_07,
            user_08,
            user_09,
            user_10,
            user_11,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_WAIFU,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_SISTER_BIG,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Orin'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_SISTER_LIL,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Momiji'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MAMA,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Koishi'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_AUNTIE,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Keiki'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_DAUGHTER,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Aya'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_GRANDDAUGHTER,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Mayumi'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_NIECE,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Keine'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MISTRESS,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Kaguya'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MAID,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Hatate'),
                    ],
                ),
            ],
            [
                (
                    RELATIONSHIP_TYPE_CO_WORKER,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Biten'),
                    ],
                ),
            ],
        ],
    )
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_01 = Relationship(
        user_id_00,
        user_id_02,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    relationship_02 = Relationship(
        user_id_00,
        user_id_03,
        RELATIONSHIP_TYPE_SISTER_LIL,
        1000,
        now,
    )
    
    relationship_03 = Relationship(
        user_id_00,
        user_id_04,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1000,
        now,
    )
    
    relationship_04 = Relationship(
        user_id_00,
        user_id_05,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_05 = Relationship(
        user_id_00,
        user_id_06,
        RELATIONSHIP_TYPE_MISTRESS,
        1000,
        now,
    )
    
    relationship_06 = Relationship(
        user_id_00,
        user_id_07,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    relationship_07 = Relationship(
        user_id_03,
        user_id_08,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_08 = Relationship(
        user_id_02,
        user_id_09,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1000,
        now,
    )
    
    relationship_09 = Relationship(
        user_id_05,
        user_id_10,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_10 = Relationship(
        user_id_00,
        user_id_11,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    yield (
        'do nut cut off pages if the space is small',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_00,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_01,),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_SISTER_LIL,
                (relationship_02,),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_SISTER_BIG,
                (relationship_03,),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_04,),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_MISTRESS,
                (relationship_05,),
            ),
            user_id_07 : RelationshipExtensionTrace(
                user_id_07,
                RELATIONSHIP_TYPE_MAID,
                (relationship_06,),
            ),
            user_id_08 : RelationshipExtensionTrace(
                user_id_08,
                RELATIONSHIP_TYPE_NIECE,
                (relationship_02, relationship_07),
            ),
            user_id_09 : RelationshipExtensionTrace(
                user_id_09,
                RELATIONSHIP_TYPE_AUNTIE,
                (relationship_01, relationship_08),
            ),
            user_id_10 : RelationshipExtensionTrace(
                user_id_10,
                RELATIONSHIP_TYPE_GRANDDAUGHTER,
                (relationship_04, relationship_09),
            ),
            user_id_11 : RelationshipExtensionTrace(
                user_id_11,
                RELATIONSHIP_TYPE_MAID,
                (relationship_10,),
            ),
        },
        [
            user_01,
            user_02,
            user_03,
            user_04,
            user_05,
            user_06,
            user_07,
            user_08,
            user_09,
            user_10,
            user_11,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_WAIFU,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_SISTER_BIG,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Orin'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_SISTER_LIL,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Momiji'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MAMA,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Koishi'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_AUNTIE,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Keiki'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_DAUGHTER,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Aya'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_GRANDDAUGHTER,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Mayumi'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_NIECE,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Keine'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MISTRESS,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Kaguya'),
                    ],
                ),
            ],
            [
                (
                    RELATIONSHIP_TYPE_MAID,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Biten'),
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Hatate'),
                    ],
                ),
            ],
        ],
    )
    
    relationship_00 = Relationship(
        user_id_00,
        user_id_01,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_01 = Relationship(
        user_id_00,
        user_id_02,
        RELATIONSHIP_TYPE_MAMA,
        1000,
        now,
    )
    
    relationship_02 = Relationship(
        user_id_00,
        user_id_03,
        RELATIONSHIP_TYPE_SISTER_LIL,
        1000,
        now,
    )
    
    relationship_03 = Relationship(
        user_id_00,
        user_id_04,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1000,
        now,
    )
    
    relationship_04 = Relationship(
        user_id_00,
        user_id_05,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_05 = Relationship(
        user_id_00,
        user_id_06,
        RELATIONSHIP_TYPE_MISTRESS,
        1000,
        now,
    )
    
    relationship_06 = Relationship(
        user_id_00,
        user_id_07,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    relationship_07 = Relationship(
        user_id_03,
        user_id_08,
        RELATIONSHIP_TYPE_DAUGHTER,
        1000,
        now,
    )
    
    relationship_08 = Relationship(
        user_id_02,
        user_id_09,
        RELATIONSHIP_TYPE_SISTER_BIG,
        1000,
        now,
    )
    
    relationship_09 = Relationship(
        user_id_00,
        user_id_10,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    relationship_10 = Relationship(
        user_id_00,
        user_id_11,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    relationship_11 = Relationship(
        user_id_00,
        user_id_12,
        RELATIONSHIP_TYPE_MAID,
        1000,
        now,
    )
    
    yield (
        'do let the last to split if there is enough space',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_00,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_MAMA,
                (relationship_01,),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_SISTER_LIL,
                (relationship_02,),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_SISTER_BIG,
                (relationship_03,),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_DAUGHTER,
                (relationship_04,),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_MISTRESS,
                (relationship_05,),
            ),
            user_id_07 : RelationshipExtensionTrace(
                user_id_07,
                RELATIONSHIP_TYPE_MAID,
                (relationship_06,),
            ),
            user_id_08 : RelationshipExtensionTrace(
                user_id_08,
                RELATIONSHIP_TYPE_NIECE,
                (relationship_02, relationship_07),
            ),
            user_id_09 : RelationshipExtensionTrace(
                user_id_09,
                RELATIONSHIP_TYPE_AUNTIE,
                (relationship_01, relationship_08),
            ),
            user_id_10 : RelationshipExtensionTrace(
                user_id_10,
                RELATIONSHIP_TYPE_MAID,
                (relationship_09,),
            ),
            user_id_11 : RelationshipExtensionTrace(
                user_id_11,
                RELATIONSHIP_TYPE_MAID,
                (relationship_10,),
            ),
            user_id_12 : RelationshipExtensionTrace(
                user_id_12,
                RELATIONSHIP_TYPE_MAID,
                (relationship_11,),
            ),
        },
        [
            user_01,
            user_02,
            user_03,
            user_04,
            user_05,
            user_06,
            user_07,
            user_08,
            user_09,
            user_10,
            user_11,
            user_12,
        ],
        0,
        [
            [
                (
                    RELATIONSHIP_TYPE_WAIFU,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Reisen'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_SISTER_BIG,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Orin'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_SISTER_LIL,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Momiji'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MAMA,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Koishi'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_AUNTIE,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Keiki'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_DAUGHTER,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Aya'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_NIECE,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Keine'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MISTRESS,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Kaguya'),
                    ],
                ),
                (
                    RELATIONSHIP_TYPE_MAID,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Biten'),
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Eirin'),
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Hatate'),
                    ],
                ),
            ],
            [
                (
                    RELATIONSHIP_TYPE_MAID,
                    [
                        (RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE, 'Mayumi'),
                    ],
                ),
            ],
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__create_relationship_listing_pages_legacy(relationship_extension_traces, users, guild_id):
    """
    Tests whether ``create_relationship_listing_pages_legacy`` works as intended.
    
    Parameters
    ----------
    relationship_extension_traces : ``None | dict<int, RelationshipExtensionTrace>``
        Relationship extension traces to render.
    
    users : ``None | list<ClientUserBase>``
        User of each relationship.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    output : `None | list<list<(int, list<(int, str)>)>>`
    """
    output = create_relationship_listing_pages_legacy(relationship_extension_traces, users, guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    return output
