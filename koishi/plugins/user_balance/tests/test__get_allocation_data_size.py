import vampytest

from ..allocation_feature_ids import (
    ALLOCATION_FEATURE_ID_GAME_21, ALLOCATION_FEATURE_ID_MARKET_PLACE, ALLOCATION_FEATURE_ID_NONE,
    get_allocation_data_size
)


def _iter_options():
    yield ALLOCATION_FEATURE_ID_GAME_21, 0
    yield ALLOCATION_FEATURE_ID_MARKET_PLACE, 8
    yield ALLOCATION_FEATURE_ID_NONE, 0


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_allocation_data_size(allocation_feature_id):
    """
    Tests whether ``get_allocation_data_size`` works as intended.
    
    Parameters
    ----------
    allocation_feature_id : `int`
        Allocation feature identifier to get data size for.
    
    Returns
    -------
    output : `int`
    """
    output = get_allocation_data_size(allocation_feature_id)
    vampytest.assert_instance(output, int)
    return output
