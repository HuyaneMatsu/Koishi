import vampytest
from hata import ClientUserBase, GuildProfile, User

from ..relationship_completion import select_first_user_for_value


def _iter_options():
    user_id_0 = 202501270020
    user_id_1 = 202501270021
    user_id_2 = 202501270022
    
    guild_id = 202501270023
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    user_1 = User.precreate(user_id_1, name = 'Rin')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Orin')
    
    user_2 = User.precreate(user_id_2, name = 'Utsuho')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Okuu')
    

    yield (
        [user_0, user_1, user_2],
        'Sa',
        0,
        user_0,
    )
    
    yield (
        [user_0, user_1, user_2],
        'Ok',
        0,
        None,
    )
    
    yield (
        [user_0, user_1, user_2],
        'Ok',
        guild_id,
        user_2,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__select_first_user_for_value(users, value, guild_id):
    """
    Tests whether ``select_first_user_for_value`` works as intended.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The users to filter from.
    
    value : `None | str`
        Value to filter for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `None | ClientUserBase`
    """
    output = select_first_user_for_value(users, value, guild_id)
    vampytest.assert_instance(output, ClientUserBase, nullable = True)
    return output
