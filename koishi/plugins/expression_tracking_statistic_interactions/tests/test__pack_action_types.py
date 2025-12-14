import vampytest

from ..helpers import pack_action_types


def _iter_options():
    yield (1, 2), 6
    yield (3,), 8


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__pack_action_types(action_types):
    """
    Parameters
    ----------
    action_types : `tuple<int>`
        The unpacked action types.
    
    Returns
    -------
    output : `int`
    """
    output = pack_action_types(action_types)
    vampytest.assert_instance(output, int)
    return output
