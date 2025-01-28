from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ....bot_utils.constants import RELATIONSHIP_VALUE_DEFAULT

from ..helpers import calculate_relationship_value
from ..relationship import Relationship
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    user_id_0 = 202501060000
    user_id_1 = 202501060001
    user_id_2 = 202501060002
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 2000, now)
    relationship_1 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000, now)
    relationship_2 = Relationship(user_id_2, user_id_0, RELATIONSHIP_TYPE_MAMA, 1000, now)
    
    yield (
        user_id_0,
        0,
        None,
        RELATIONSHIP_VALUE_DEFAULT,
    )
    
    yield (
        user_id_0,
        -4000,
        [
            relationship_0,
            relationship_1,
        ],
        RELATIONSHIP_VALUE_DEFAULT,
    )
    
    yield (
        user_id_0,
        1000,
        [
            relationship_0,
            relationship_1,
        ],
        2449,
    )
    
    yield (
        user_id_0,
        1000,
        [
            relationship_2,
        ],
        1000,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_relationship_value(user_id, base_relationship_value, relationships):
    """
    Tests whether ``calculate_relationship_value`` works as intended.
    
    Parameters
    ----------
    user_id  : `int`
        The user's identifier.
    
    base_relationship_value : `int`
        The base value for the user's relationships.
    
    relationships : `None | list<Relationship>`
        The user's relationships.
    
    Returns
    -------
    output : `int`
    """
    output = calculate_relationship_value(user_id, base_relationship_value, relationships)
    vampytest.assert_instance(output, int)
    return output
