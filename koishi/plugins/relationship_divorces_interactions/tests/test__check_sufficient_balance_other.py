import vampytest
from hata import GuildProfile, User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_sufficient_balance_other


def _iter_options__passing():
    user_id = 202502050012
    guild_id = 202502050013
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield 1000, 1000, 2, user, guild_id
    yield 1000, 1001, 2, user, guild_id


def _iter_options__failing():
    user_id = 202502050014
    guild_id = 202502050015
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield 1000, 999, 2, user, guild_id


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_sufficient_balance_other(
    required_balance, available_balance, new_relationship_slot_count, user, guild_id
):
    """
    Tests whether ``check_sufficient_balance_other`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required balance to buy the relationship slot.
    
    available_balance : `int`
        The available balance of the user.
    
    new_relationship_slot_count : `int`
        The new relationship slot count.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_sufficient_balance_other(required_balance, available_balance, new_relationship_slot_count, user, guild_id)
