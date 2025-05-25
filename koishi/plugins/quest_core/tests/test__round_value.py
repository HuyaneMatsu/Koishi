import vampytest

from ..quest_batch_generation import round_value


def _iter_options():
    yield 100, 10, 100
    yield 104, 10, 100
    yield 106, 10, 110


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__round_value(value, require_multiple_of):
    """
    Tests whether ``round_value`` works as intended.
    
    Parameters
    ----------
    value : `int`
        Value to round.
    
    require_multiple_of : `int`
        Value to require the output to be multiple of.
    
    Returns
    -------
    output : `int`
    """
    output = round_value(value, require_multiple_of)
    vampytest.assert_instance(output, int)
    return output
