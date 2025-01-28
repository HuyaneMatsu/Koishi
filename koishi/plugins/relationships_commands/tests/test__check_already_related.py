from datetime import datetime as DateTime, timezone as TimeZone 

import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, Relationship

from ..checks import check_already_related


def _iter_options__passing():
    user_id_0 = 202501030040
    user_id_1 = 202501030041
    user_id_2 = 202501030042
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Alice')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        None,
        True,
        user_0,
        user_1,
        0,
    )
    
    yield (
        None,
        False,
        user_0,
        user_1,
        0,
    )
    
    yield (
        [
            Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 500, now),
        ],
        True,
        user_0,
        user_1,
        0,
    )


def _iter_options__failing():
    user_id_0 = 202501030043
    user_id_1 = 202501030044
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        [
            Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 500, now),
        ],
        True,
        user_0,
        user_1,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_already_related(relationship_listing, checked_at_creation, source_user, target_user, guild_id):
    """
    Tests whether ``check_already_related`` works as intended.
    
    Parameters
    ----------
    relationship_listing : `None | list<Relationship>`
        The relationship_listing of one of the users.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_already_related(relationship_listing, checked_at_creation, source_user, target_user, guild_id)
