import vampytest

from ..helpers import get_affinity_multiplier


def _iter_options():
    yield 202501050010, 202501051011, 1.8800000000000001
    yield 202501051012, 202501053013, 1.75


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_affinity_multiplier(source_user_id, target_user_id):
    """
    Tests whether ``get_affinity_multiplier`` works as intended. 
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    Returns
    -------
    output : `float`
    """
    output = get_affinity_multiplier(source_user_id, target_user_id)
    vampytest.assert_instance(output, float)
    return output
