import vampytest

from ..adventurer_rank_info_generation import get_user_adventurer_rank_up_credibility


def _iter_options():
    yield 0, 256
    yield 1, 512
    yield 2, 1024


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_adventurer_rank_up_credibility(level):
    """
    Tests whether ``get_user_adventurer_rank_up_credibility`` works as intended.
    
    Parameters
    ----------
    level : `int`
        The user's current level.
    
    Returns
    -------
    output : `int`
    """
    output = get_user_adventurer_rank_up_credibility(level)
    vampytest.assert_instance(level, int)
    return output
