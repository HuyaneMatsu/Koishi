import vampytest

from ..helpers import unpack_action_types


def _iter_options():
    yield 0, ()
    yield 6, (1, 2)
    yield 8, (3,)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__unpack_action_types(packed):
    """
    Parameters
    ----------
    packed : `int`
        The packed action types.
    
    Returns
    -------
    output : `tuple<int>`
    """
    output = unpack_action_types(packed)
    vampytest.assert_instance(output, tuple)
    return output
