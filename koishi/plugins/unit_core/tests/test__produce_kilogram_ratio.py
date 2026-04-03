import vampytest

from ..content_building import produce_kilogram_ratio


def _iter_options():
    yield 10, 20, '0.010 / 0.020 kg'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_kilogram_ratio(weight_0, weight_1):
    """
    Tests whether ``produce_kilogram_ratio`` works as intended.
    
    Parameters
    ----------
    weight_0 : `int`
        Used weight
    
    weight_1 : `int`
        Total weight.
    
    Returns
    -------
    output : `str`
    """
    into = [*produce_kilogram_ratio(weight_0, weight_1)]
    
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
