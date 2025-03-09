import vampytest

from config import KOISHI_ID

from ..helpers import get_affinity_percent


def _iter_options():
    yield 202501050010_000000, 202501051011_000000, 14
    yield 202501051012_000000, 202501053013_000000, 68
    yield 202503010000_000000, KOISHI_ID, 100
    yield KOISHI_ID, 202503010001_000000, 100


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
