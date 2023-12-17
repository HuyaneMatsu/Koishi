import vampytest

from ..interactions import process_custom_message


def _iter_options():
    yield None, None
    yield '', None
    yield 'aya', 'aya'
    yield '\nayaya\n\nayaya\n', 'ayaya\nayaya'
    yield '\n\n', None


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__process_custom_message(input_value):
    """
    Tests whether ``process_custom_message`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        Value to test with.
    
    Returns
    -------
    output : `None | str`
    """
    return process_custom_message(input_value)
