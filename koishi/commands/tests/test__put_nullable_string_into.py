import vampytest

from ..action_asset_information_generation import _put_nullable_string_into


def _iter_options():
    yield 'koishi', 'mister', '**koishi**'
    yield None, 'mister', '*mister*'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_nullable_string_into(string, default):
    """
    Tests whether ``_put_nullable_string_into`` works as intended.
    
    Parameters
    ----------
    string : `None | str`
        String to put.
    default : `str`
        Default to use if `string` is `None`
    
    Returns
    -------
    output : `str`
    """
    output = _put_nullable_string_into(string, default, [])
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
