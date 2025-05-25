import vampytest

from ..utils import (
    USER_STAT_NAME_FULL_BEDROOM, USER_STAT_NAME_FULL_CHARM, USER_STAT_NAME_FULL_CUTENESS, USER_STAT_NAME_FULL_DEFAULT,
    USER_STAT_NAME_FULL_HOUSEWIFE, USER_STAT_NAME_FULL_LOYALTY, get_user_stat_name_full_for_index
)


def _iter_options():
    yield -1, USER_STAT_NAME_FULL_DEFAULT
    yield 0, USER_STAT_NAME_FULL_HOUSEWIFE
    yield 1, USER_STAT_NAME_FULL_CUTENESS
    yield 2, USER_STAT_NAME_FULL_BEDROOM
    yield 3, USER_STAT_NAME_FULL_CHARM
    yield 4, USER_STAT_NAME_FULL_LOYALTY
    yield 5, USER_STAT_NAME_FULL_DEFAULT


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_stat_name_full_for_index(stat_index):
    """
    Tests whether ``get_user_stat_name_full_for_index`` works as intended.
    
    Parameters
    ----------
    stat_index : `int`
        The stat's index.
    
    Returns
    -------
    output : `str`
    """
    output = get_user_stat_name_full_for_index(stat_index)
    vampytest.assert_instance(output, str)
    return output
