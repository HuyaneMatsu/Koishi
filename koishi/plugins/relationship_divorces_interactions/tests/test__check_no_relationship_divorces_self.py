import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_no_relationship_divorces_self


def _iter_options__passing():
    yield 1


def _iter_options__failing():
    yield 0
    yield -1


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_no_relationship_divorces_self(relationship_slots):
    """
    Tests whether ``check_no_relationship_divorces_self`` works as intended.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The current relationship divorce count.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_no_relationship_divorces_self(relationship_slots)
