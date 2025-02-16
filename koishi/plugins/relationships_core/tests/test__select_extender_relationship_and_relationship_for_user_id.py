from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import ClientUserBase

from ..relationship import Relationship
from ..relationship_completion import select_extender_relationship_and_relationship_for_user_id
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    user_id_0 = 202501270040
    user_id_1 = 202501270041
    user_id_2 = 202501270042
    user_id_3 = 202501270043
    user_id_4 = 202501270044
    user_id_5 = 202501270045
    user_id_6 = 202501270046
    user_id_7 = 202501270047
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_2, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_3 = Relationship(user_id_0, user_id_4, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_4 = Relationship(user_id_5, user_id_4, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_5 = Relationship(user_id_4, user_id_6, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    yield (
        [
            (relationship_0, None),
            (relationship_1, None),
            (relationship_2, None),
        ],
        user_id_0,
        (None, relationship_0),
    )
    
    yield (
        [
            (relationship_0, None),
            (relationship_1, None),
            (relationship_2, None),
        ],
        user_id_6,
        None,
    )
    
    yield (
        [
            (relationship_0, None),
            (relationship_1, None),
            (relationship_2, None),
            (relationship_3, [relationship_4, relationship_5]),
        ],
        user_id_6,
        (relationship_3, relationship_5),
    )
    
    yield (
        [
            (relationship_0, None),
            (relationship_1, None),
            (relationship_2, None),
            (relationship_3, [relationship_4, relationship_5]),
        ],
        user_id_7,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test_select_extender_relationship_and_relationship_for_user_id(
    relationship_listing_with_extend, user_id
):
    """
    Tests whether ``select_extender_relationship_and_relationship_for_user_id`` works as intended.
    
    Parameters
    ----------
    relationship_listing_with_extend : `None | list<(Relationship, None | list<Relationship>)>`
        The relationship listing with its extends to get the user identifiers from.
    
    user_id : `int`
        The user identifier to select relationship with.
    
    Returns
    -------
    output : `None | (Relationship, ClientUserBase)`
    """
    output = select_extender_relationship_and_relationship_for_user_id(
        relationship_listing_with_extend, user_id
    )
    vampytest.assert_instance(output, tuple, nullable = True)
    if (output is not None):
        vampytest.assert_eq(len(output), 2)
        vampytest.assert_instance(output[0], Relationship, nullable = True)
        vampytest.assert_instance(output[1], Relationship)
    
    return output
