from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..helpers import iter_select_relationships
from ..relationship import Relationship
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_SISTER_LIL, RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    user_id_0 = 202501240010
    user_id_1 = 202501240011
    user_id_2 = 202501240012
    user_id_3 = 202501240013
    user_id_4 = 202501240014
    
    
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
        [],
    )
    
    # look for waifu but no waifu
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_WAIFU,
        [relationship_0, relationship_1, relationship_3],
        [],
    )
    
    # look for wife, has wife
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_WAIFU,
        [relationship_0, relationship_1, relationship_2, relationship_3],
        [relationship_2],
    )
    
    # look for lil-sis, hit all & reversed
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_SISTER_LIL,
        [relationship_0, relationship_1, relationship_2, relationship_3],
        [
            relationship_0,
            relationship_1,
            relationship_3,
        ],
    )
    
    # look for big-sis, do not match reversed
    yield (
        user_id_0,
        RELATIONSHIP_TYPE_SISTER_BIG,
        [relationship_0, relationship_1, relationship_2, relationship_3],
        [],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_select_relationships(user_id, relationship_type, relationship_listing):
    """
    Tests whether ``iter_select_relationships`` works as intended.
    
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
    output : `list<Relationship>`
    """
    output = [*iter_select_relationships(user_id, relationship_type, relationship_listing)]
    
    for element in output:
        vampytest.assert_instance(element, Relationship)
    
    return output
