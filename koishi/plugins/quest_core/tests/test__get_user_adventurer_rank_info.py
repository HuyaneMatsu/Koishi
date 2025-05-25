import vampytest

from ..adventurer_rank_info import AdventurerRankInfo
from ..adventurer_rank_info_generation import get_user_adventurer_rank_info


def _iter_options():
    yield 0, (0, 1)
    yield 15, (0, 1)
    
    yield 16, (1, 1)
    yield 31, (1, 1)
    
    yield 32, (2, 2)
    yield 63, (2, 2)
    
    yield 64, (3, 2)
    yield 127, (3, 2)
    
    yield 128, (4, 3)
    yield 255, (4, 3)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_user_adventurer_rank_info(credibility):
    """
    Tests whether ``get_user_adventurer_rank_info`` works as intended.
    
    Parameters
    ----------
    credibility : `int`
        The user's credibility.
    
    Returns
    -------
    level_and_quest_limit : `(int, int)`
    """
    output = get_user_adventurer_rank_info(credibility)
    vampytest.assert_instance(output, AdventurerRankInfo)
    return output.level, output.quest_limit
