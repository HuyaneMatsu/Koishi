import vampytest
from hata import GuildProfile, User

from ..relationship_completion import _make_suggestions


def _iter_options():
    user_id_0 = 202501070010_000000
    user_id_1 = 202501070011_000000
    user_id_2 = 202501070012_000000
    
    guild_id = 202501070014_000000
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_0.guild_profiles[guild_id] = GuildProfile(nick = 'Sato')
    
    user_1 = User.precreate(user_id_1, name = 'Rin')
    user_1.guild_profiles[guild_id] = GuildProfile(nick = 'Orin')
    
    user_2 = User.precreate(user_id_2, name = 'Utsuho')
    user_2.guild_profiles[guild_id] = GuildProfile(nick = 'Okuu')
    
    yield (
        [user_0, user_1, user_2],
        None,
        0,
        [
            ('Rin', str(user_id_1)),
            ('Satori', str(user_id_0)),
            ('Utsuho', str(user_id_2)),
        ],
    )
    
    yield (
        [user_0, user_1, user_2],
        None,
        guild_id,
        [
            ('Okuu', str(user_id_2)),
            ('Orin', str(user_id_1)),
            ('Sato', str(user_id_0)),
        ],
    )
    
    yield (
        [user_0, user_1, user_2],
        'ri',
        0,
        [
            ('Rin', str(user_id_1)),
            ('Satori', str(user_id_0)),
        ],
    )
    
    yield (
        [user_0, user_1, user_2],
        'ri',
        guild_id,
        [
            ('Orin', str(user_id_1)),
            ('Sato', str(user_id_0)),
        ],
    )
    
    yield (
        [user_0, user_1, user_2],
        'ok',
        0,
        None,
    )
    
    yield (
        [user_0, user_1, user_2],
        'ok',
        guild_id,
        [
            ('Okuu', str(user_id_2)),
        ],
    )
    
    yield (
        [user_0, user_1, user_2],
        'ok',
        guild_id,
        [
            ('Okuu', str(user_id_2)),
        ],
    )
    
    yield (
        [user_0, user_1, user_2],
        str(user_id_1),
        0,
        [
            ('Rin', str(user_id_1)),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__make_suggestions(users, value, guild_id):
    """
    Tests whether ``_make_suggestions`` works as intended.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The users to make suggestions for.
    
    value : `None | str`
        Value to get suggestions for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : `list<(str, str)>`
    """
    output = _make_suggestions(users, value, guild_id)
    vampytest.assert_instance(output, list, nullable = True)
    return output
