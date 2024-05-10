import vampytest

from ..helpers import _merge_values_with_values


def _iter_options():
    yield None, (1,), (1,)
    yield (1, 3), (2,), (1, 2, 3)
    yield (1,), (1,), (1,)
    yield None, (), (None)
    yield (1, 3), (2, 3, 4), (1, 2, 3, 4)
    yield None, (2, 2), (2,)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test___merge_values_with_values(old_values, values):
    """
    Tests whether ``old_values`` works as intended.
    
    Parameters
    ----------
    old_values : `None | tuple<object>`
        Values to merge to.
    values : `tuple<object>`
        Value to merge.
    
    Returns
    -------
    new_values : `None | tuple<object>`
    """
    return _merge_values_with_values(old_values, values)
