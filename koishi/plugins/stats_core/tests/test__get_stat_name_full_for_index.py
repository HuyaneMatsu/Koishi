import vampytest

from ..utils import (
    STAT_NAME_FULL_BEDROOM, STAT_NAME_FULL_CHARM, STAT_NAME_FULL_CUTENESS, STAT_NAME_FULL_DEFAULT,
    STAT_NAME_FULL_HOUSEWIFE, STAT_NAME_FULL_LOYALTY, get_stat_name_full_for_index
)


def _iter_options():
    yield -1, STAT_NAME_FULL_DEFAULT
    yield 0, STAT_NAME_FULL_HOUSEWIFE
    yield 1, STAT_NAME_FULL_CUTENESS
    yield 2, STAT_NAME_FULL_BEDROOM
    yield 3, STAT_NAME_FULL_CHARM
    yield 4, STAT_NAME_FULL_LOYALTY
    yield 5, STAT_NAME_FULL_DEFAULT


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_stat_name_full_for_index(stat_index):
    """
    Tests whether ``get_stat_name_full_for_index`` works as intended.
    
    Parameters
    ----------
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    output : `str`
    """
    output = get_stat_name_full_for_index(stat_index)
    vampytest.assert_instance(output, str)
    return output
