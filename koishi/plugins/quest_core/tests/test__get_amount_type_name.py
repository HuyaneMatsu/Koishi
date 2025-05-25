import vampytest

from ..amount_types import AMOUNT_TYPE_COUNT, get_amount_type_name


def _iter_options():
    yield -1
    yield AMOUNT_TYPE_COUNT


@vampytest._(vampytest.call_from(_iter_options()))
def test__get_amount_type_name(amount_type):
    """
    Tests whether the ``get_amount_type_name`` works as intended.
    
    Parameters
    ----------
    amount_type : `int`
        Amount type to get name of.
    """
    output = get_amount_type_name(amount_type)
    vampytest.assert_instance(output, str)
