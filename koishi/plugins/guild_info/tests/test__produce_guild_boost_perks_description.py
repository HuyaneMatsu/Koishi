from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import Guild

from ..content_building import produce_guild_boost_perks_description


def _iter_options():
    guild_id = 202511260000
    guild = Guild.precreate(
        guild_id,
    )
    
    yield (
        guild,
        False,
        (
            '## Boost perks\n'
            '**Boost level: 0**\n'
            '**Badges:** *none*\n'
            '**Others:** *none*\n'
            '\n'
            '**Attachment size limit: 8MB**\n'
            '**Bitrate limit: 96 kbps**\n'
            '**Concurrent activities: 2**\n'
            '**Emoji limit: 50**\n'
            '**Sticker limit: 5**\n'
            '**Soundboard sound limit: 8**\n'
            '**Granted features:** *none*\n'
            '**Screen share frame limit: 30**\n'
            '**Screen share resolution: 720p**\n'
            '**Stage channel viewer limit: 50**'
        ),
    )
    
    
    guild_id = 202511260001
    
    guild = Guild.precreate(
        guild_id,
        boost_count = 15,
        boost_level = 3,
    )
    
    yield (
        guild,
        False,
        (
            '## Boost perks\n'
            '**Boost level: 3**\n'
            '**Badges:** *none*\n'
            '**Others:** *none*\n'
            '\n'
            '**Attachment size limit: 100MB**\n'
            '**Bitrate limit: 384 kbps**\n'
            '**Concurrent activities: unlimited**\n'
            '**Emoji limit: 250**\n'
            '**Sticker limit: 60**\n'
            '**Soundboard sound limit: 48**\n'
            '**Granted features:** banner, banner animated, icon animated, invite splash, invite vanity url, role icons\n'
            '**Screen share frame limit: 60**\n'
            '**Screen share resolution: 1080p**\n'
            '**Stage channel viewer limit: 300**'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_guild_boost_perks_description(guild, even_if_empty):
    """
    Tests whether ``produce_guild_boost_perks_description`` works as intended.
    
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
        produce_guild_boost_perks_description,
        elapsed_time = elapsed_time_mock,
    )
    
    output = [*mocked(guild, even_if_empty)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
