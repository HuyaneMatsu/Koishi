import vampytest

from ..adventurer_rank_info import AdventurerRankInfo
from ..adventurer_rank_info_generation import get_guild_adventurer_rank_info


def _iter_options():
    yield 0, (0, 2)
    yield 1023, (0, 2)
    
    yield 1024, (1, 3)
    yield 2047, (1, 3)
    
    yield 2048, (2, 5)
    yield 4095, (2, 5)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_guild_adventurer_rank_info(credibility):
    """
    Tests whether ``get_guild_adventurer_rank_info`` works as intended.
    
    Parameters
    ----------
    credibility : `int`
        The guild's credibility.
    
    Returns
    -------
    level_and_quest_limit : `(int, int)`
    """
    output = get_guild_adventurer_rank_info(credibility)
    vampytest.assert_instance(output, AdventurerRankInfo)
    return output.level, output.quest_limit
