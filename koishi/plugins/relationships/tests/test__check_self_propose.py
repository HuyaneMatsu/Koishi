import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_self_propose


def _iter_options__passing():
    source_user = User.precreate(202501010010)
    target_user = User.precreate(202501010011)
    
    yield source_user, target_user


def _iter_options__failing():
    source_user = User.precreate(202501010010)
    yield source_user, source_user


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_self_propose(source_user, target_user):
    """
    Tests whether ``check_self_propose`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_self_propose(source_user, target_user)
