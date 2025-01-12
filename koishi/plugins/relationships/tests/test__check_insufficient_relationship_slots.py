import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_insufficient_relationship_slots


def _iter_options__passing():
    yield 0, 0, 1
    yield 5, 0, 6
    yield 0, 5, 6
    yield 5, 5, 11


def _iter_options__failing():
    yield 6, 0, 6
    yield 0, 6, 6
    yield 5, 6, 11
    yield 6, 5, 11


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_insufficient_relationship_slots(relationship_count, relationship_request_count, relationship_slots):
    """
    Tests whether ``check_insufficient_relationship_slots`` works as intended.
    
    Parameters
    ----------
    relationship_count : `int`
        How much relationships the user has.
    
    relationship_request_count : `int`
        How much relationship requests the user has.
    
    relationship_slots : `int`
        How much relationships the user can have.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_insufficient_relationship_slots(relationship_count, relationship_request_count, relationship_slots)
