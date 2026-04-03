from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ..relationship import Relationship
from ..relationship_completion import _filter_relationships_unset_outgoing
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG, RELATIONSHIP_TYPE_UNSET


def _iter_options():
    user_id_0 = 202501070020
    user_id_1 = 202501070021
    user_id_2 = 202501070022
    user_id_3 = 202501070023
    user_id_4 = 202501070024
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000, now)
    relationship_1 = Relationship(user_id_2, user_id_0, RELATIONSHIP_TYPE_UNSET, 1900, now)
    relationship_2 = Relationship(user_id_0, user_id_3, RELATIONSHIP_TYPE_UNSET, 1800, now)
    relationship_3 = Relationship(user_id_4, user_id_0, RELATIONSHIP_TYPE_UNSET, 1700, now)
    relationship_3.target_investment = 600
    
    yield (
        user_id_0,
        [relationship_0, relationship_1, relationship_2, relationship_3],
        [relationship_2, relationship_3],
    )
    
    yield (
        user_id_2,
        [relationship_2],
        None,
    )
    
    yield (
        user_id_4,
        [relationship_3],
        [relationship_3],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__filter_relationships_unset_outgoing(user_id, relationships):
    """
    Tests whether ``_filter_relationships_unset_outgoing`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to exclude.
    
    relationships : `list<Relationship>`
        The relationships to get the user identifiers from.
    
    Returns
    -------
    relationships : `None | list<Relationship>`
    """
    output = _filter_relationships_unset_outgoing(user_id, relationships)
    vampytest.assert_instance(output, list, nullable = True)
    return output
