import vampytest

from ..adventurer_rank_info import AdventurerRankInfo
from ..adventurer_rank_info_generation import get_user_adventurer_rank_info


def _iter_options():
    yield 0, (0, 1)
    yield 255, (0, 1)
    
    yield 256, (1, 2)
    yield 511, (1, 2)
    
    yield 512, (2, 2)
    yield 1023, (2, 2)


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
