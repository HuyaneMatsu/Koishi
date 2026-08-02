import vampytest

from ..constants import REASON_ALLOWED_LENGTH_THRESHOLD
from ..helpers import process_reason


def _iter_options():
    yield (
        None,
        None,
    )
    
    yield (
        'a',
        'a',
    )
    
    yield (
        'a' * REASON_ALLOWED_LENGTH_THRESHOLD,
        'a' * REASON_ALLOWED_LENGTH_THRESHOLD,
    )
    
    yield (
        'a' * (REASON_ALLOWED_LENGTH_THRESHOLD + 1),
        'a' * REASON_ALLOWED_LENGTH_THRESHOLD + ' ...',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__process_reason(reason):
    """
    Tests whether ``process_reason`` works as intended.
    
    Parameters
    ----------
    reason : `None | str`
        The reason to validate.
    
    Returns
    -------
    output : `None | str`
    """
    output = process_reason(reason)
    vampytest.assert_instance(output, str, nullable = True)
    return output
