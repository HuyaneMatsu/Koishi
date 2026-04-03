from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import select_relationship
from ..relationship import Relationship
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    user_id_0 = 202501240000
    user_id_1 = 202501240001
    user_id_2 = 202501240002
    user_id_3 = 202501240003
    user_id_4 = 202501240004
    
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_3 = Relationship(user_id_4, user_id_0, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    
    # no input
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_WAIFU,
        None,
        None,
    )
    
    # look for waifu but no waifu
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_WAIFU,
        [relationship_0, relationship_1],
        None,
    )
    
    # look for wife, has wife
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_WAIFU,
        [relationship_0, relationship_1, relationship_2, relationship_3],
        relationship_2,
    )
    
    # look for lil-sis, hit first
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_SISTER_LIL,
        [relationship_0, relationship_1, relationship_2, relationship_3],
        relationship_0,
    )
    
    # look for lil-sis, match reversed
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_SISTER_LIL,
        [relationship_2, relationship_3],
        relationship_3,
    )
    
    # look for big-sis, do not match reversed
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_SISTER_BIG,
        [relationship_0, relationship_1, relationship_2, relationship_3],
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_relationship(user_id, relationship_type, relationship_listing):
    """
    Tests whether ``select_relationship`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to filter based on.
    
    relationship_type : `int`
        The relation type to look for.
    
    relationship_listing : `None | list<Relationship>`
        The relationships to select from.
    
    Returns
    -------
    output : `None | Relationship`
    """
    output = select_relationship(user_id, relationship_type, relationship_listing)
    vampytest.assert_instance(output, Relationship, nullable = True)
    return output
