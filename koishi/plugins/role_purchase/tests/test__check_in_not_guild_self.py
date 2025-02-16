import vampytest
from hata import Guild, GuildProfile, Role, User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_not_in_guild_self


def _iter_options__passing():
    role_id = 202502140030
    guild_id = 202502140031
    user_id = 202502140032
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    guild = Guild.precreate(guild_id)
    
    yield role, user, [guild]
    yield role, user, [guild]


def _iter_options__failing():
    role_id = 202502140033
    guild_id = 202502140034
    user_id = 202502140035
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    user = User.precreate(user_id)
    guild = Guild.precreate(guild_id)
    
    yield role, user, [guild]
    yield role, user, [guild]


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_not_in_guild_self(role, user, cache):
    """
    Tests whether ``check_not_in_guild_self`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : ``ClientUserBase``
        The user the who is purchasing the role.
    
    cache : `None | list<Guild>`
        Additional objects to keep in cache.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_not_in_guild_self(role, user)
