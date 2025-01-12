import vampytest

from ..helpers import get_affinity_percent


def _iter_options():
    yield 202501050010, 202501051011, 22
    yield 202501051012, 202501053013, 35


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_affinity_percent(source_user_id, target_user_id):
    """
    Tests whether ``get_affinity_percent`` works as intended. 
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    Returns
    -------
    output : `int`
    """
    output = get_affinity_percent(source_user_id, target_user_id)
    vampytest.assert_instance(output, int)
    return output
