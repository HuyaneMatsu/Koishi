import vampytest
from hata import Guild

from ...quest_core import AdventurerRankInfo

from ..content_builders import build_quest_board_header_description


def _iter_options():
    yield (
        202505230000,
        'Orin\'s dance house',
        AdventurerRankInfo(2, 6),
        6,
        (
            '# Orin\'s dance house\'s quest board\n'
            '\n'
            'Guild rank: F\n'
            'Quest count: 6'
        ),
    )
    
    yield (
        202505240040,
        'Orin\'s dance house',
        AdventurerRankInfo(2, 6),
        4,
        (
            '# Orin\'s dance house\'s quest board\n'
            '\n'
            'Guild rank: F\n'
            'Quest count: 4 / 6'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_quest_board_header_description(guild_id, guild_name, adventurer_info, quest_count):
    """
    Tests whether ``build_quest_board_header_description`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier.
    
    guild_name : `str`
        Guild name.
    
    adventurer_info : ``AdventurerRankInfo``
        Information about the guild's adventurer rank.
    
    quest_count : `int`
        The amount of quests the guild currently has.
    
    Returns
    -------
    output : `str`
    """
    guild = Guild.precreate(guild_id, name = guild_name)
    
    output = build_quest_board_header_description(guild, adventurer_info, quest_count)
    vampytest.assert_instance(output, str)
    return output
