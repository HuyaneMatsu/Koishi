import vampytest

from ..embed_builders import _render_weight_into


def _iter_options():
    yield 12, '0.012'
    yield 132334, '132.334'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_weight_into(weight):
    """
    Tests whether ``_render_weight_into`` works as intended.
    
    Parameters
    ----------
    weight : `int`
        Weight in grams.
    
    Returns
    -------
    output : `str`
    """
    into = _render_weight_into(weight, [])
    
    vampytest.assert_instance(into, list)
    for element in into:
        vampytest.assert_instance(element, str)
    
    return ''.join(into)
