import vampytest

from ..building import _put_strings_into


def _iter_options():
    yield ('koishi', ), 'mister', '**koishi**'
    yield ('koishi', 'satori'), 'mister', '**koishi**, **satori**'
    yield None, 'mister', '*mister*'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_strings_into(strings, default):
    """
    Tests whether ``_put_strings_into`` works as intended.
    
    Parameters
    ----------
    strings : `None | tuple<str>`
        Strings to put.
    default : `str`
        Default to use if `strings` is `None`
    
    Returns
    -------
    output : `str`
    """
    output = _put_strings_into(strings, default, [])
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
