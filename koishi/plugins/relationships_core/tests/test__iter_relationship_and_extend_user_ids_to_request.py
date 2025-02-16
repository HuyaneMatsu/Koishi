from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..relationship import Relationship
from ..relationship_completion import iter_relationship_and_extend_user_ids_to_request
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_WAIFU


def _iter_options():
    user_id_0 = 202501090020
    user_id_1 = 202501090021
    user_id_2 = 202501090022
    user_id_3 = 202501090023
    user_id_4 = 202501090024
    user_id_5 = 202501090025
    user_id_6 = 202501090026
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_2, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_3 = Relationship(user_id_0, user_id_4, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_4 = Relationship(user_id_4, user_id_0, RELATIONSHIP_TYPE_WAIFU, 2000, now)
    relationship_5 = Relationship(user_id_5, user_id_4, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_6 = Relationship(user_id_4, user_id_6, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    yield (
        user_id_0,
        [
            (relationship_0, None),
            (relationship_1, None),
            (relationship_2, None),
        ],
        [user_id_1, user_id_2, user_id_3],
    )
    
    yield (
        user_id_0,
        [
            (relationship_0, None),
            (relationship_1, None),
            (relationship_2, None),
            (relationship_3, [relationship_5, relationship_6]),
        ],
        [user_id_1, user_id_2, user_id_3, user_id_4, user_id_5, user_id_6],
    )
    
    yield (
        user_id_0,
        [
            (relationship_0, None),
            (relationship_1, None),
            (relationship_2, None),
            (relationship_4, [relationship_5, relationship_6]),
        ],
        [user_id_1, user_id_2, user_id_3, user_id_4, user_id_5, user_id_6],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_relationship_and_extend_user_ids_to_request(
    excluded_user_id, relationship_listing_with_extend
):
    """
    Tests whether ``iter_relationship_and_extend_user_ids_to_request`` works as intended.
    
    Parameters
    ----------
    excluded_user_id : `int`
        The user identifier to exclude.
    
    relationship_listing_with_extend : `None | list<(Relationship, None | list<Relationship>)>`
        The relationship listing with their extend to get the user identifiers from.
    
    Returns
    -------
    output : `list<int>`
    """
    output = sorted(iter_relationship_and_extend_user_ids_to_request(
        excluded_user_id, relationship_listing_with_extend,
    ))
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
