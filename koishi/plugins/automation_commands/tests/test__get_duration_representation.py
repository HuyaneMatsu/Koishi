import vampytest

from ..representation_getters import get_duration_representation


def _iter_options():
    yield 0, '0 second'
    yield 3601, '1 hour, 1 second'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_duration_representation(value):
    """
    Tests whether ``get_duration_representation`` works as intended.
    
    Parameters
    ----------
    value : `int`
        Value to get representation for.
    
    Returns
    -------
    output : `str`
    """
    output = get_duration_representation(value)
    vampytest.assert_instance(output, str)
    return output
