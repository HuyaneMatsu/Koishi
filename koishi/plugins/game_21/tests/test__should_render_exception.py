__all__ = ()

import vampytest
from hata import DiscordException, ERROR_CODES

from ..helpers import should_render_exception


def _iter_options():
    exception = ValueError()
    yield exception, True
    
    exception = ConnectionError()
    yield exception, False
    
    exception = DiscordException(None, None, None, None)
    exception.code = ERROR_CODES.missing_access
    yield exception, False
    
    exception = DiscordException(None, None, None, None)
    exception.code = ERROR_CODES.unknown_account
    yield exception, True
    
    exception = DiscordException(None, None, None, None)
    exception.code = ERROR_CODES.unknown_interaction
    yield exception, False


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__should_render_exception(exception):
    """
    Tests whether ``should_render_exception`` works as intended.
    
    Parameters
    ----------
    Exception : `BaseException`
        The exception to decide about.
    
    Returns
    -------
    output : `bool`
    """
    output = should_render_exception(exception)
    vampytest.assert_instance(output, bool)
    return output
