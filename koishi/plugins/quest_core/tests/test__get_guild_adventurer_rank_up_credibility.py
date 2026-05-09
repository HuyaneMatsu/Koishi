import vampytest

from ..adventurer_rank_info_generation import get_guild_adventurer_rank_up_credibility


def _iter_options():
    yield 0, 1024
    yield 1, 2048
    yield 2, 4096


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_guild_adventurer_rank_up_credibility(level):
    """
    Tests whether ``get_guild_adventurer_rank_up_credibility`` works as intended.
    
    Parameters
    ----------
    level : `int`
        The guild's current level.
    
    Returns
    -------
    output : `int`
    """
    output = get_guild_adventurer_rank_up_credibility(level)
    vampytest.assert_instance(level, int)
    return output
