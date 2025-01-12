import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_can_propose_to_bot


def _iter_options__passing():
    user_id_0 = 202501100000
    user_id_1 = 202501100001
    
    user_0 = User.precreate(user_id_0, name = 'Satori', bot = True)
    user_1 = User.precreate(user_id_1, name = 'Koishi', bot = False)
    
    yield (
        user_0,
        0,
        1,
        0,
    )
    
    yield (
        user_1,
        2,
        1,
        0,
    )


def _iter_options__failing():
    user_id_0 = 202501100002
    
    user_0 = User.precreate(user_id_0, name = 'Satori', bot = True)
    
    yield (
        user_0,
        1,
        1,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_can_propose_to_bot(target_user, target_relationship_count, target_relationship_slots, guild_id):
    """
    Tests whether ``check_can_propose_to_bot`` works as intended.
    
    Parameters
    ----------
    target_user : ``ClientUserBase``
        The target user.
    
    target_relationship_count : `int`
        The amount of relationships the target user have.
    
    target_relationship_slots : `int`
        The amount of relationships the target user can have.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_can_propose_to_bot(target_user, target_relationship_count, target_relationship_slots, guild_id)
