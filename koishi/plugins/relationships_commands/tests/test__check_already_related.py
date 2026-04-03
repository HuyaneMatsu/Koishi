from datetime import datetime as DateTime, timezone as TimeZone 

import vampytest
from hata import Component, User, create_text_display

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_SISTER_LIL, Relationship

from ..checks import check_already_related


def _iter_options():
    user_id_0 = 202501030040
    user_id_1 = 202501030041
    user_id_2 = 202501030042
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Alice')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        None,
        True,
        user_0,
        user_1,
        0,
        None,
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        None,
        False,
        user_0,
        user_1,
        0,
        None,
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_SISTER_LIL, 500, now),
        True,
        user_1,
        user_0,
        0,
        None,
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 500, now),
        True,
        user_0,
        user_1,
        0,
        [
            create_text_display(
                'You are already the mama of Koishi.'
            ),
        ],
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 500, now),
        True,
        user_1,
        user_0,
        0,
        [
            create_text_display(
                'You are already the daughter of Satori.'
            ),
        ],
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 500, now),
        True,
        user_0,
        user_1,
        0,
        [
            create_text_display(
                f'You are already the daughter of Koishi.'
            ),
        ],
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA, 500, now),
        True,
        user_1,
        user_0,
        0,
        [
            create_text_display(
                'You are already the mama of Satori.'
            ),
        ],
    )
    
    # The existing relationship should be masked
    yield (
        RELATIONSHIP_TYPE_MAMA,
        Relationship(user_id_1, user_id_0, RELATIONSHIP_TYPE_MAMA | RELATIONSHIP_TYPE_SISTER_LIL, 500, now),
        True,
        user_1,
        user_0,
        0,
        [
            create_text_display(
                'You are already the mama of Satori.'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__check_already_related(
    relationship_type, relationship, checked_at_creation, source_user, target_user, guild_id
):
    """
    Tests whether ``check_already_related`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
    
    relationship : ``None | Relationship``
        The existing relationship between the two users.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``None | list<Component>``
    """
    output = check_already_related(
        relationship_type, relationship, checked_at_creation, source_user, target_user, guild_id
    )
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Component)
        
    return output
