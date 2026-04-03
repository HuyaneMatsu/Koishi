from datetime import datetime as DateTime

import vampytest
from hata import Guild, GuildFeature

from ..content_building import produce_guild_info_description


def _iter_options():
    guild_id = 202511210000
    guild = Guild.precreate(
        guild_id,
    )
    
    yield (
        guild,
        False,
        (
            '## Guild information\n'
            '**Created**: 2015-01-01 00:00:48 [*2 years ago*]'
        ),
    )
    
    
    guild_id = 202511210001
    guild = Guild.precreate(
        guild_id,
        features = [
            GuildFeature.activity_list_disabled,
        ],
    )
    
    yield (
        guild,
        False,
        (
            '## Guild information\n'
            '**Created**: 2015-01-01 00:00:48 [*2 years ago*]\n'
            '**Other features**: activity list disabled'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_guild_info_description(guild, even_if_empty):
    """
    Tests whether ``produce_guild_info_description`` works as intended.
    
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
        vampytest.assert_eq(guild.created_at, input_created_at)
        return '2 years'
    
    mocked = vampytest.mock_globals(
        produce_guild_info_description,
        elapsed_time = elapsed_time_mock,
    )
    
    output = [*mocked(guild, even_if_empty)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
