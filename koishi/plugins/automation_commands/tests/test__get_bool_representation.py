import vampytest

from ..representation_getters import get_bool_representation


def _iter_options():
    yield True, 'enabled'
    yield False, 'disabled'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_bool_representation(value):
    """
    Tests whether ``get_bool_representation`` works as intended.
    
    Parameters
    ----------
    value : `bool`
        Value to get representation for.
    
    Returns
    -------
    output : `str`
    """
    output = get_bool_representation(value)
    vampytest.assert_instance(output, str)
    return output
