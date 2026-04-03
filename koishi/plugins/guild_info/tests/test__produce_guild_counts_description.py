import vampytest
from hata import Channel, ChannelType, Guild, Role, User

from ..content_building import produce_guild_counts_description


def _iter_options():
    guild_id = 202511210002
    guild = Guild.precreate(
        guild_id,
    )
    
    yield (
        guild,
        False,
        (
            '## Counts\n'
            '**Users: 0**\n'
            '**Roles: 0**'
        ),
    )
    
    
    guild_id = 202511210003
    user_id_0 = 202511210004
    user_id_1 = 202511210005
    user_id_2 = 202511210006
    role_id_0 = 202511210007
    role_id_1 = 202511210008
    channel_id_0 = 202511210009
    
    guild = Guild.precreate(
        guild_id,
        users = [
            User.precreate(user_id_0),
            User.precreate(user_id_1),
            User.precreate(user_id_2),
        ],
        user_count = 3,
        roles = [
            Role.precreate(role_id_0),
            Role.precreate(role_id_1),
        ],
        channels = [
            Channel.precreate(channel_id_0, channel_type = ChannelType.guild_text),
        ],
    )
    
    yield (
        guild,
        False,
        (
            '## Counts\n'
            '**Users: 3**\n'
            '**Roles: 2**\n'
            '**Text channels: 1**'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_guild_counts_description(guild, even_if_empty):
    """
    Tests whether ``produce_guild_counts_description`` works as intended.
    
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
    output = [*produce_guild_counts_description(guild, even_if_empty)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
