import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, RelationshipRequest

from ..checks import check_already_proposing


def _iter_options__passing():
    user_id_0 = 202501030060
    user_id_1 = 202501030061
    user_id_2 = 202501030062
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Alice')
    
    yield (
        None,
        user_1,
        0,
    )
    
    yield (
        [
            RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 500),
        ],
        user_1,
        0,
    )


def _iter_options__failing():
    user_id_0 = 202501030063
    user_id_1 = 202501030064
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    
    yield (
        [
            RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 500),
        ],
        user_1,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_already_proposing(source_relationship_request_listing, target_user, guild_id):
    """
    Tests whether ``check_already_proposing`` works as intended.
    
    Parameters
    ----------
    source_relationship_request_listing : `None | list<RelationshipRequest>`
        The relationship requests of the source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_already_proposing(source_relationship_request_listing, target_user, guild_id)
