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

from ..relationship_listing_rendering_wide import create_relationship_listing_pages_wide


def _iter_options():
    user_id_00 = 202601250200
    user_id_01 = 202601250201
    user_id_02 = 202601250202
    user_id_03 = 202601250203
    user_id_04 = 202601250204
    user_id_05 = 202601250205
    user_id_06 = 202601250206
    user_id_07 = 202601250207
    user_id_08 = 202601250208
    user_id_09 = 202601250209
    user_id_10 = 202601250210
    user_id_11 = 202601250211
    user_id_12 = 202601250212
    user_id_13 = 202601250213
    user_id_14 = 202601250214
    user_id_15 = 202601250215
    user_id_16 = 202601250216
    user_id_17 = 202601250217
    user_id_18 = 202601250218
    user_id_19 = 202601250219
    user_id_20 = 202601250220
    user_id_21 = 202601250221
    user_id_22 = 202601250222
    
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
    
    user_13 = User.precreate(
        user_id_13,
        name = 'Tewi',
    )
    
    user_14 = User.precreate(
        user_id_14,
        name = 'Parsee',
    )
    
    user_15 = User.precreate(
        user_id_15,
        name = 'Youmu',
    )
    
    user_16 = User.precreate(
        user_id_16,
        name = 'Yuyuko',
    )
    
    user_17 = User.precreate(
        user_id_17,
        name = 'Dai',
    )
    
    user_18 = User.precreate(
        user_id_18,
        name = 'Rumia',
    )
    
    user_19 = User.precreate(
        user_id_19,
        name = 'Mystia',
    )
    
    user_20 = User.precreate(
        user_id_20,
        name = 'Yuuka',
    )
    
    user_21 = User.precreate(
        user_id_21,
        name = 'Alice',
    )
    
    user_22 = User.precreate(
        user_id_22,
        name = 'Akyuu',
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
                    (
                        (
                            3,
                            RELATIONSHIP_TYPE_MAMA,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Reisen',
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
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                        (
                            3,
                            RELATIONSHIP_TYPE_MAMA,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Reisen',
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
        'two',
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
                    (
                        (
                            3,
                            RELATIONSHIP_TYPE_MAMA,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Koishi',
                ),
                (
                    (
                        (
                            3,
                            RELATIONSHIP_TYPE_MAMA,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Reisen',
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
        'two in a single group, one with alternative',
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
                    (
                        (
                            3,
                            RELATIONSHIP_TYPE_MAMA,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Reisen',
                ),
                (
                    (
                        (
                            3,
                            RELATIONSHIP_TYPE_MAMA,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_IN_LAW,
                        ),
                    ),
                    'Koishi',
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
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Reisen',
                ),
                (
                    (
                        (
                            3,
                            RELATIONSHIP_TYPE_MAMA,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Koishi',
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
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_02 = Relationship(
        user_id_00,
        user_id_03,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_03 = Relationship(
        user_id_00,
        user_id_04,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_04 = Relationship(
        user_id_00,
        user_id_05,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_05 = Relationship(
        user_id_00,
        user_id_06,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_06 = Relationship(
        user_id_00,
        user_id_07,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_07 = Relationship(
        user_id_00,
        user_id_08,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_08 = Relationship(
        user_id_00,
        user_id_09,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_09 = Relationship(
        user_id_00,
        user_id_10,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_10 = Relationship(
        user_id_00,
        user_id_11,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_11 = Relationship(
        user_id_00,
        user_id_12,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_12 = Relationship(
        user_id_00,
        user_id_13,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_13 = Relationship(
        user_id_00,
        user_id_14,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_14 = Relationship(
        user_id_00,
        user_id_15,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_15 = Relationship(
        user_id_00,
        user_id_16,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_16 = Relationship(
        user_id_00,
        user_id_17,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_17 = Relationship(
        user_id_00,
        user_id_18,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_18 = Relationship(
        user_id_00,
        user_id_19,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_19 = Relationship(
        user_id_00,
        user_id_20,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_20 = Relationship(
        user_id_00,
        user_id_21,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    relationship_21 = Relationship(
        user_id_00,
        user_id_22,
        RELATIONSHIP_TYPE_WAIFU,
        1000,
        now,
    )
    
    
    yield (
        'multiple pages',
        {
            user_id_01 : RelationshipExtensionTrace(
                user_id_01,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_00,),
            ),
            user_id_02 : RelationshipExtensionTrace(
                user_id_02,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_01,),
            ),
            user_id_03 : RelationshipExtensionTrace(
                user_id_03,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_02,),
            ),
            user_id_04 : RelationshipExtensionTrace(
                user_id_04,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_03,),
            ),
            user_id_05 : RelationshipExtensionTrace(
                user_id_05,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_04,),
            ),
            user_id_06 : RelationshipExtensionTrace(
                user_id_06,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_05,),
            ),
            user_id_07 : RelationshipExtensionTrace(
                user_id_07,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_06,),
            ),
            user_id_08 : RelationshipExtensionTrace(
                user_id_08,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_07,),
            ),
            user_id_09 : RelationshipExtensionTrace(
                user_id_09,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_08,),
            ),
            user_id_10 : RelationshipExtensionTrace(
                user_id_10,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_09,),
            ),
            user_id_11 : RelationshipExtensionTrace(
                user_id_11,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_10,),
            ),
            user_id_12 : RelationshipExtensionTrace(
                user_id_12,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_11,),
            ),
            user_id_13 : RelationshipExtensionTrace(
                user_id_13,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_12,),
            ),
            user_id_14 : RelationshipExtensionTrace(
                user_id_14,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_13,),
            ),
            user_id_15 : RelationshipExtensionTrace(
                user_id_15,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_14,),
            ),
            user_id_16 : RelationshipExtensionTrace(
                user_id_16,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_15,),
            ),
            user_id_17 : RelationshipExtensionTrace(
                user_id_17,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_16,),
            ),
            user_id_18 : RelationshipExtensionTrace(
                user_id_18,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_17,),
            ),
            user_id_19 : RelationshipExtensionTrace(
                user_id_19,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_18,),
            ),
            user_id_20 : RelationshipExtensionTrace(
                user_id_20,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_19,),
            ),
            user_id_21 : RelationshipExtensionTrace(
                user_id_21,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_20,),
            ),
            user_id_22 : RelationshipExtensionTrace(
                user_id_22,
                RELATIONSHIP_TYPE_WAIFU,
                (relationship_21,),
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
            user_13,
            user_14,
            user_15,
            user_16,
            user_17,
            user_18,
            user_19,
            user_20,
            user_21,
            user_22,
        ],
        0,
        [
            [
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Akyuu',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Alice',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Aya',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Biten',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Dai',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Eirin',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Hatate',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Kaguya',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Keiki',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Keine',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Koishi',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Mayumi',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Momiji',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Mystia',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Orin',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Parsee',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Reisen',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Rumia',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Tewi',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Youmu',
                ),
            ],
            [
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Yuuka',
                ),
                (
                    (
                        (
                            0,
                            RELATIONSHIP_TYPE_WAIFU,
                            RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
                        ),
                    ),
                    'Yuyuko',
                ),
            ],
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test__create_relationship_listing_pages_wide(relationship_extension_traces, users, guild_id):
    """
    Tests whether ``create_relationship_listing_pages_wide`` works as intended.
    
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
    output : `None | list<list<(int, list<(int, int, str)>)>>`
    """
    output = create_relationship_listing_pages_wide(relationship_extension_traces, users, guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    return output
