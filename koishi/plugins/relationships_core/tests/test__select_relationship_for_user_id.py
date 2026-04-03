from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..relationship import Relationship
from ..relationship_completion import select_relationship_for_user_id
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG


def _iter_options():
    user_id_0 = 202501270030
    user_id_1 = 202501270031
    user_id_2 = 202501270032
    user_id_3 = 202501270033
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_3, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_2, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        user_id_0,
        relationship_0,
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        user_id_1,
        relationship_1,
    )
    
    yield (
        [relationship_0, relationship_1, relationship_2],
        user_id_2,
        relationship_2,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_relationship_for_user_id(relationship_listing, user_id):
    """
    Tests whether ``select_relationship_for_user_id`` works as intended.
    
    Parameters
    ----------
    relationship_listing : `list<Relationship>`
        Relationships to select from.
    
    user_id : `int`
        The user identifier to select relationship with.
    
    Returns
    -------
    output : `None | Relationship`
    """
    output = select_relationship_for_user_id(relationship_listing, user_id)
    vampytest.assert_instance(output, Relationship, nullable = True)
    return output
