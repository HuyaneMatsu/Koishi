import vampytest

from ..component_builders import produce_used


def _iter_options():
    yield (
        'energy',
        130,
        100,
        'Used energy: 100 / 130',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_used(name, initial, exhausted):
    """
    Tests whether ``produce_used`` works as intended.
    
    Parameters
    ----------
    name : `str`
        The name of the used value.
    
    initial : `int`
        Initial value.
    
    exhaust : `int`
        The exhausted amount.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_used(name, initial, exhausted)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
