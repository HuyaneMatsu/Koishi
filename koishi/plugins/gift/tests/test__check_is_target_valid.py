import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_is_target_valid


def _iter_options__passing():
    user_id_0 = 202502230010
    user_id_1 = 202502230011
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    # different users
    yield (
        user_0,
        user_1,
    )


def _iter_options__failing():
    user_id_0 = 202502230014
    user_id_1 = 202502230015
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    
    # no target user
    yield (
        user_0,
        None,
    )
    
    # same
    yield (
        user_1,
        user_1,
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_is_target_valid(source_user, target_user):
    """
    Tests whether ``check_is_target_valid`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is gifting.
    
    target_user : `None | ClientUserBase`
        The targeted user if any.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_is_target_valid(source_user, target_user)
