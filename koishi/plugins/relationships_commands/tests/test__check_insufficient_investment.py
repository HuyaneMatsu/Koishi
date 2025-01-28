import vampytest
from hata.ext.slash import InteractionAbortedError

from ..checks import check_insufficient_investment


def _iter_options__passing():
    yield 199, 200
    yield 200, 200


def _iter_options__failing():
    yield 201, 200


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_insufficient_investment(relationship_value, investment):
    """
    Tests whether ``check_insufficient_investment`` works as intended.
    
    Parameters
    ----------
    relationship_value : `int`
        The minimal value the user needs to propose with to start the relationship.
    
    investment : `int`
        Investment to propose with.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_insufficient_investment(relationship_value, investment)
