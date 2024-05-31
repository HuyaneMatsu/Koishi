import vampytest

from ..constants import CHOICE_DEFAULT
from ..representation_getters import get_choice_representation


def _iter_options():
    yield None, CHOICE_DEFAULT
    yield 'miau', 'miau'


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_choice_representation(value):
    """
    Tests whether ``get_choice_representation`` works as intended.
    
    Parameters
    ----------
    value : `None | str`
        Value to get representation for.
    
    Returns
    -------
    output : `str`
    """
    output = get_choice_representation(value)
    vampytest.assert_instance(output, str)
    return output
