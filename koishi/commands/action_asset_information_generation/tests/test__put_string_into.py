import vampytest

from ..building import _put_string_into


def _iter_options():
    yield 'koishi', '*', '*koishi*'
    yield 'mister', '**', '**mister**'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_string_into(string, affix):
    """
    Tests whether ``_put_string_into`` works as intended.
    
    Parameters
    ----------
    string : `str`
        String to put.
    affix : `str`
        Affix to use.
    
    Returns
    -------
    output : `str`
    """
    output = _put_string_into(string, affix, [])
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
