import vampytest

from ..helpers import get_relationship_divorce_reduction_required_balance


def _iter_options():
    yield 1223312111565, 1, 9036
    yield 1223312111565, 2, 21324


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_relationship_divorce_reduction_required_balance(user_id, divorce_count):
    """
    Tests whether ``get_relationship_divorce_reduction_required_balance`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    divorce_count : `int`
        The amount of divorces of the user.
    
    Returns
    -------
    output : `int`
    """
    output = get_relationship_divorce_reduction_required_balance(user_id, divorce_count)
    vampytest.assert_instance(output, int)
    return output
