from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Guild, GuildProfile, User

from ..content_building import EMOJI_HEART_GIFT, produce_guild_boosters_description


def _iter_options():
    guild_id = 202511210042
    guild = Guild.precreate(
        guild_id,
    )
    
    yield (
        guild,
        False,
        (
            ''
        ),
    )
    
    
    guild_id = 202511210043
    user_id_0 = 202511210044
    user_id_1 = 202511210045
    user_id_2 = 202511210046
    
    
    user_0 = User.precreate(user_id_0, name = 'koishi')
    user_0.guild_profiles[guild_id] = GuildProfile(boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    user_1 = User.precreate(user_id_1, name = 'Satori')
    user_1.guild_profiles[guild_id] = GuildProfile(boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    user_2 = User.precreate(user_id_2, name = 'Parsee')
    user_2.guild_profiles[guild_id] = GuildProfile(boosts_since = DateTime(2016, 5, 14, tzinfo = TimeZone.utc))
    
    guild = Guild.precreate(
        guild_id,
        boost_count = 3,
        users = [
            user_0,
            user_1,
            user_2,
        ],
    )
    
    yield (
        guild,
        False,
        (
            f'## Most awesome people of the guild\n'
            f'{EMOJI_HEART_GIFT} 3 boosts | 3 people {EMOJI_HEART_GIFT}\n'
            f'\n'
            f'- **koishi**, since: 2 years\n'
            f'- **Satori**, since: 2 years\n'
            f'- **Parsee**, since: 2 years\n'
            f'\n'
            f'-# The displayed users might be just a subset of the reality'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_guild_boosters_description(guild, even_if_empty):
    """
    Tests whether ``produce_guild_boosters_description`` works as intended.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild in context.
    
    even_if_empty : `bool`
        Whether the field should be added even if it would be empty. Not applicable for this function.
    
    Returns
    -------
    output : `str`
    """
    def elapsed_time_mock(input_created_at):
        nonlocal guild
        vampytest.assert_instance(input_created_at, DateTime)
        vampytest.assert_eq(DateTime(2016, 5, 14, tzinfo = TimeZone.utc), input_created_at)
        return '2 years'
    
    mocked = vampytest.mock_globals(
        produce_guild_boosters_description,
        elapsed_time = elapsed_time_mock,
    )
    
    output = [*mocked(guild, even_if_empty)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
