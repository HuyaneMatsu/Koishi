import vampytest

from ..utils import produce_weight


def _iter_options():
    yield 12, '0.012'
    yield 132334, '132.334'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_weight(weight):
    """
    Tests whether ``produce_weight`` works as intended.
    
    Parameters
    ----------
    weight : `int`
        Weight in grams.
    
    Returns
    -------
    output : `str`
    """
    into = [*produce_weight(weight)]
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
