import vampytest

from ..shared_constants import REASON_ALLOWED_LENGTH_MAX
from ..shared_helpers import process_reason


def _iter_options():
    yield None, None
    yield '', None
    yield 'a', 'a'
    yield 'a' * REASON_ALLOWED_LENGTH_MAX, 'a' * REASON_ALLOWED_LENGTH_MAX
    yield 'a' * (REASON_ALLOWED_LENGTH_MAX + 1), 'a' * REASON_ALLOWED_LENGTH_MAX + ' ...'



@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__process_reason(input_value):
    """
    Tests whether ``process_reason`` works as intended.
    
    Parameters
    ----------
    input_value : `None | str`
        The value to test with.
    
    Returns
    -------
    output : `None | str`
    """
    return process_reason(input_value)
