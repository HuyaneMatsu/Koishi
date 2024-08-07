import vampytest
from hata import Guild, GuildProfile, User

from ..rendering import build_user_listing_description


def _iter_options():
    user_0 = User.precreate(202408060000, name = 'Remilia')
    user_1 = User.precreate(202408060001, name = 'Sakuya')
    guild = Guild.precreate(202408060002)
    guild_profile_1 = GuildProfile(nick = 'Suyu')
    user_1.guild_profiles[guild.id] = guild_profile_1
    
    
    yield (
        [],
        None,
        (
            '_ _'
        ),
    )
    
    yield (
        [user_0, user_1],
        guild,
        (
            f'{user_0.name}\n'
            f'{guild_profile_1.nick}'
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_user_listing_description(users, guild):
    """
    Tests whether ``build_user_listing_description`` works as intended.

    Parameters
    ----------
    users : `list<ClientUserBase>`
        The users to list.
    guild : `None | Guild`
        The respective guild.
    
    Returns
    -------
    output : `str`
    """
    output = build_user_listing_description(users, guild)
    vampytest.assert_instance(output, str)
    return output
