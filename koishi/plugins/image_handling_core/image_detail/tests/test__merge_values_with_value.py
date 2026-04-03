import vampytest

from ..helpers import _merge_values_with_value



def _iter_options():
    yield None, 1, (1,)
    yield (1, 3), 2, (1, 2, 3)
    yield (1,), 1, (1,)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__merge_values_with_value(old_values, value):
    """
    Tests whether ``old_values`` works as intended.
    
    Parameters
    ----------
    old_values : `None | tuple<object>`
        Values to merge to.
    value : `object`
        Value to merge.
    
    Returns
    -------
    new_values : `tuple<object>`
    """
    return _merge_values_with_value(old_values, value)
