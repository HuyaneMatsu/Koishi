import vampytest
from hata import GuildProfile, User

from ...quest_core import AdventurerRankInfo

from ..content_builders import produce_linked_quest_header_description


def _iter_options():
    yield (
        202505230001,
        'Fonsered',
        202505230002,
        'Fons',
        AdventurerRankInfo(1, 1),
        1,
        (
            '# Fons\'s quests\n'
            '\n'
            'User rank: G\n'
            'Quest count: 1 / 1'
        ),
    )
    
    yield (
        202505230003,
        'Fonsered',
        0,
        None,
        AdventurerRankInfo(1, 1),
        0,
        (
            '# Fonsered\'s quests\n'
            '\n'
            'User rank: G\n'
            'Quest count: 0 / 1'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_linked_quest_header_description(user_id, user_name, guild_id, user_nick, adventurer_info, quest_count):
    """
    Tests whether ``produce_linked_quest_header_description`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        User identifier.
    
    user_name : `str`
        User name.
    
    guild_id : `int`
        The respective guild's identifier the command is used.
    
    user_nick : `None | str`
        The user's nick name in the guild.
    
    adventurer_info : ``AdventurerRankInfo``
        Information about the user's adventurer rank.
    
    quest_count : `int`
        The amount of quests the user currently has.
    
    Returns
    -------
    output : `str`
    """
    user = User.precreate(user_id, name = user_name)
    
    if guild_id and (user_nick is not None):
        user.guild_profiles[guild_id] = GuildProfile(nick = user_nick)
    
    output = [*produce_linked_quest_header_description(user, guild_id, adventurer_info, quest_count)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
