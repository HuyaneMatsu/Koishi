import vampytest
from hata import GuildProfile, User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_no_relationship_divorces_other


def _iter_options__passing():
    user_id = 202502050008
    guild_id = 202502050009
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    yield 1, user, guild_id


def _iter_options__failing():
    user_id = 202502050010
    guild_id = 202502050011
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield 0, user, guild_id
    yield -1, user, guild_id


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_no_relationship_divorces_other(relationship_slots, user, guild_id):
    """
    Tests whether ``check_no_relationship_divorces_other`` works as intended.
    
    Parameters
    ----------
    relationship_divorces : `int`
        The current relationship divorce count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_no_relationship_divorces_other(relationship_slots, user, guild_id)
