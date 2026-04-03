import vampytest

from ..constants import AMOUNT_TYPE_NAME_DEFAULT
from ..amount_types import AMOUNT_TYPE_WEIGHT, produce_amount_type_with_name


def _iter_options():
    yield (
        1 << 63,
        ''.join([repr(1 << 63), ' (', AMOUNT_TYPE_NAME_DEFAULT, ')']),
    )
    
    yield (
        AMOUNT_TYPE_WEIGHT,
        ''.join([repr(AMOUNT_TYPE_WEIGHT), ' (', 'weight', ')']),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_amount_type_with_name(amount_type):
    """
    Tests whether ``produce_amount_type_with_name`` works as intended.
    
    Parameters
    ----------
    amount_type : `int`
        Amount type.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_amount_type_with_name(amount_type)]
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
