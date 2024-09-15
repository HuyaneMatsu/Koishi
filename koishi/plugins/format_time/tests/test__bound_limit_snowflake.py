import vampytest

from ..constants import ID_MAX, ID_MIN
from ..helpers import bound_limit_snowflake


def _iter_options():
    yield 100000000, 100000000
    yield ID_MAX, ID_MAX
    yield ID_MAX + 1, ID_MAX
    yield ID_MIN, ID_MIN,
    yield ID_MIN -1, ID_MIN


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__bound_limit_snowflake(input_value):
    """
    Tests whether ``bound_limit_snowflake`` works as intended.
    
    Parameters
    ----------
    input_value : `int`
        Value to test with.
    
    Returns
    -------
    output : `int`
    """
    output = bound_limit_snowflake(input_value)
    vampytest.assert_instance(output, int)
    return output
