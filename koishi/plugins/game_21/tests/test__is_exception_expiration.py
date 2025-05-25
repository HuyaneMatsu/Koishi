__all__ = ()

import vampytest
from hata import DiscordException, ERROR_CODES

from ..helpers import is_exception_expiration


def _iter_options():
    exception = ValueError()
    yield exception, False
    
    exception = ConnectionError()
    yield exception, False
    
    exception = DiscordException(None, None, None, None)
    exception.code = ERROR_CODES.missing_access
    yield exception, False
    
    exception = DiscordException(None, None, None, None)
    exception.code = ERROR_CODES.unknown_account
    yield exception, False
    
    exception = DiscordException(None, None, None, None)
    exception.code = ERROR_CODES.unknown_interaction
    yield exception, True


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__is_exception_expiration(exception):
    """
    Tests whether ``is_exception_expiration`` works as intended.
    
    Parameters
    ----------
    Exception : `BaseException`
        The exception to decide about.
    
    Returns
    -------
    output : `bool`
    """
    output = is_exception_expiration(exception)
    vampytest.assert_instance(output, bool)
    return output
