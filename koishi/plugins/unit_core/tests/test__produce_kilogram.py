import vampytest

from ..content_building import produce_kilogram


def _iter_options():
    yield 12, '0.012 kg'
    yield 132334, '132.334 kg'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_kilogram(weight):
    """
    Tests whether ``produce_kilogram`` works as intended.
    
    Parameters
    ----------
    weight : `int`
        Weight in grams.
    
    Returns
    -------
    output : `str`
    """
    into = [*produce_kilogram(weight)]
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
