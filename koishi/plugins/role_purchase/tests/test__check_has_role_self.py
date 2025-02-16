import vampytest
from hata import GuildProfile, Role, User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_has_role_self


def _iter_options__passing():
    role_id = 202502140004
    guild_id = 202502140005
    user_id = 202502140006
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    user = User.precreate(user_id)
    
    yield role, user


def _iter_options__failing():
    role_id = 202502140007
    guild_id = 202502140008
    user_id = 202502140009
    
    role = Role.precreate(role_id, name = 'Nyan', guild_id = guild_id)
    user = User.precreate(user_id)
    user.guild_profiles[guild_id] = GuildProfile(role_ids = [role_id])
    
    yield role, user


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_has_role_self(role, user):
    """
    Tests whether ``check_has_role_self`` works as intended.
    
    Parameters
    ----------
    role : ``Role``
        The role to be purchased.
    
    user : ``ClientUserBase``
        The user the who is purchasing the role.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_has_role_self(role, user)
