from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..relationship import Relationship
from ..relationship_completion import _iter_relationship_user_ids_to_request
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG


def _iter_options():
    user_id_0 = 202501070000
    user_id_1 = 202501070001
    user_id_2 = 202501070002
    user_id_3 = 202501070003
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_2, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    
    yield (
        user_id_0,
        [relationship_0, relationship_1, relationship_2],
        [user_id_1, user_id_2, user_id_3],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_relationship_user_ids_to_request(user_id, relationships):
    """
    Tests whether ``_iter_relationship_user_ids_to_request`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to exclude.
    
    relationships : `list<Relationship>`
        The relationships to get the user identifiers from.
    
    Returns
    -------
    output : `list<int>`
    """
    output = sorted(_iter_relationship_user_ids_to_request(user_id, relationships))
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
