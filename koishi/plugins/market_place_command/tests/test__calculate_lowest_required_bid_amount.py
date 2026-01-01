import vampytest

from ..helpers import calculate_lowest_required_bid_amount


def _iter_options():
    yield 0, 10
    yield 10, 20
    yield 10000, 10100


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__calculate_lowest_required_bid_amount(current_highest_bid):
    """
    Tests whether ``calculate_lowest_required_bid_amount`` works as intended.
    
    Parameters
    ----------
    current_highest_bid : `int`
        The current highest bid amount.
    
    Returns
    -------
    output : `int`
    """
    output = calculate_lowest_required_bid_amount(current_highest_bid)
    vampytest.assert_instance(output, int)
    return output
