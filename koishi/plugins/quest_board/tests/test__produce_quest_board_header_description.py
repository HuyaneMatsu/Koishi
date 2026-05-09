import vampytest
from hata import Guild

from ...quest_core import AdventurerRankInfo

from ..content_building import produce_quest_board_header_description


def _iter_options():
    yield (
        202505230000,
        'Orin\'s dance house',
        3000,
        AdventurerRankInfo(2, 6),
        6,
        (
            '# Orin\'s dance house\'s quest board\n'
            '\n'
            'Guild rank: F (3000 / 4096)\n'
            'Quest count: 6'
        ),
    )
    
    yield (
        202505240040,
        'Orin\'s dance house',
        3000,
        AdventurerRankInfo(2, 6),
        4,
        (
            '# Orin\'s dance house\'s quest board\n'
            '\n'
            'Guild rank: F (3000 / 4096)\n'
            'Quest count: 4 / 6'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_quest_board_header_description(guild_id, guild_name, credibility, adventurer_info, quest_count):
    """
    Tests whether ``produce_quest_board_header_description`` works as intended.
    
    Parameters
    ----------
    guild_id : `int`
        Guild identifier.
    
    guild_name : `str`
        Guild name.
    
    credibility : `int`
        The amount of credibility the user has.
    
    adventurer_info : ``AdventurerRankInfo``
        Information about the guild's adventurer rank.
    
    quest_count : `int`
        The amount of quests the guild currently has.
    
    Returns
    -------
    output : `str`
    """
    guild = Guild.precreate(guild_id, name = guild_name)
    
    output = [*produce_quest_board_header_description(guild, credibility, adventurer_info, quest_count)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
