import vampytest

from ..action_asset_information_generation import _put_string_field_into


def _iter_options():
    yield 'satori', 'koishi', 'mister', 'satori: **koishi**\n'
    yield 'satori', None, 'mister', 'satori: *mister*\n'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__put_string_field_into(title, string, default):
    """
    Tests whether ``_put_string_field_into`` works as intended.
    
    Parameters
    ----------
    title : `str`
        Title to start with.
    string : `None | None`
        String to put.
    default : `str`
        Default to use if `string` is `None`
    
    Returns
    -------
    output : `str`
    """
    output = _put_string_field_into(title, string, default, [])
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
