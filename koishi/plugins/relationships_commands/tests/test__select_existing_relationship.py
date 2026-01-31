from datetime import datetime as DateTime, timezone as TimeZone 

import vampytest

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, Relationship

from ..helpers import select_existing_relationship


def _iter_options():
    user_id_0 = 202601290000
    user_id_1 = 202601290001
    user_id_2 = 202601290002
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        user_id_0,
        user_id_1,
        None,
    )
    
    relationship = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 500, now)
    
    yield (
        [
            relationship,
        ],
        user_id_0,
        user_id_1,
        None,
    )
    
    relationship = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 500, now)
    
    yield (
        [
            relationship,
        ],
        user_id_0,
        user_id_1,
        relationship,
    )
    
    relationship = Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 500, now)
    
    yield (
        [
            relationship,
        ],
        user_id_0,
        user_id_1,
        relationship,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_existing_relationship(relationship_listing, source_user_id, target_user_id):
    """
    Tests whether ``select_existing_relationship`` works as intended.
    
    Parameters
    ----------
    relationship_listing : `None | list<Relationship>`
        The relationship listing of one of the users.
    
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The targeted user's identifier.
    
    Returns
    -------
    output : ``None | Relationship``
    """
    output = select_existing_relationship(relationship_listing, source_user_id, target_user_id)
    vampytest.assert_instance(output, Relationship, nullable = True)
    return output
