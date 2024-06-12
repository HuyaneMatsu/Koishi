import vampytest

from ..flag_naming import get_kind_name


def _iter_options():
    yield False, False, 'none'
    yield False, True, 'custom',
    yield True, False, 'unicode'
    yield True, True, 'all'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_kind_name(unicode, custom):
    """
    Tests whether ``get_kind_name`` works as intended.
    
    Parameters
    ----------
    unicode : `bool`
        Whether unicode emoji parsing is allowed.
    custom : `bool`
        Whether custom emoji parsing is allowed.
    
    Returns
    -------
    output : `str`
    """
    output = get_kind_name(unicode, custom)
    vampytest.assert_instance(output, str)
    return output
