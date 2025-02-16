import vampytest
from hata import Guild, GuildProfile, Role, User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_not_in_guild_other


def _iter_options__passing():
    role_id = 202502140020
    guild_id = 202502140021
    user_id = 202502140022
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    guild = Guild.precreate(guild_id)
    
    yield role, user, 0, [guild]
    yield role, user, guild_id, [guild]


def _iter_options__failing():
    role_id = 202502140023
    guild_id = 202502140024
    user_id = 202502140015
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    user = User.precreate(user_id)
    guild = Guild.precreate(guild_id)
    
    yield role, user, 0, [guild]
    yield role, user, guild_id, [guild]


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_not_in_guild_other(role, user, guild_id, cache):
    """
    Tests whether ``check_not_in_guild_other`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : ``ClientUserBase``
        The user the who is purchasing the role.
    
    guild_id : `int`
        The respective guild's identifier.
    
    cache : `None | list<Guild>`
        Additional objects to keep in cache.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_not_in_guild_other(role, user, guild_id)
