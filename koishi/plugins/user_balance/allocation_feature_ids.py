__all__ = (
    'ALLOCATION_FEATURE_ID_GAME_21', 'ALLOCATION_FEATURE_ID_MARKET_PLACE', 'ALLOCATION_FEATURE_ID_NONE',
    'ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST'
)

ALLOCATION_FEATURE_ID_NONE = 0
ALLOCATION_FEATURE_ID_GAME_21 = 1
ALLOCATION_FEATURE_ID_MARKET_PLACE = 2
ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST = 3


def get_allocation_data_size(allocation_feature_id):
    """
    Gets the data size for the given allocation feature identifier.
    
    Parameters
    ----------
    allocation_feature_id : `int`
        Allocation feature identifier to get data size for.
    
    Returns
    -------
    data_size : `int`
    """
    if allocation_feature_id == ALLOCATION_FEATURE_ID_MARKET_PLACE:
        return 8
    
    return 0
