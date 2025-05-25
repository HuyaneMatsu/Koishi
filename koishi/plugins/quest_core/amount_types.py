__all__ = ('AMOUNT_TYPE_COUNT', 'AMOUNT_TYPE_VALUE', 'AMOUNT_TYPE_WEIGHT', 'get_amount_type_name',)

from .constants import AMOUNT_TYPE_NAME_DEFAULT

AMOUNT_TYPE_NONE = 0
AMOUNT_TYPE_COUNT = 1
AMOUNT_TYPE_WEIGHT = 2
AMOUNT_TYPE_VALUE = 3



AMOUNT_TYPE_NAMES = {
    AMOUNT_TYPE_NONE : 'none',
    AMOUNT_TYPE_COUNT : 'count',
    AMOUNT_TYPE_WEIGHT : 'weight',
    AMOUNT_TYPE_VALUE : 'value',
}


def get_amount_type_name(amount_type):
    """
    Gets the name of the given amount type.
    
    Parameters
    ----------
    amount_type : `int`
        Amount type to get name of.
    
    Returns
    -------
    amount_type_name : `str`
    """
    return AMOUNT_TYPE_NAMES.get(amount_type, AMOUNT_TYPE_NAME_DEFAULT)
