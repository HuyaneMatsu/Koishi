import vampytest
from hata import GuildProfile, User
from hata.ext.slash import InteractionAbortedError

from ..checks import check_sufficient_available_balance_other


def _iter_options__passing():
    user = User.precreate(202503150008, name = 'Sariel')
    guild_id = 202503150009
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Angel')
    
    yield 1000, 1000, 2, 12, user, guild_id
    yield 1000, 1001, 2, 12, user, guild_id


def _iter_options__failing():
    user = User.precreate(202503150004, name = 'Sariel')
    guild_id = 202503150005
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Angel')
    
    yield 1000, 999, 2, 12, user, guild_id


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_sufficient_available_balance_other(
    required_balance, available_balance, stat_index, stat_value_after, user, guild_id
):
    """
    Tests whether ``check_sufficient_available_balance_other`` works as intended.
    
    Parameters
    ----------
    required_balance : `int`
        The required amount of balance for the purchase.
    
    available_balance : `int`
        Available balance.
    
    stat_index : `int`
        The index of the stat.
    
    stat_value_after : `int`
        The stats value after upgrade.
    
    user : ``ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The current guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_sufficient_available_balance_other(
        required_balance, available_balance, stat_index, stat_value_after, user, guild_id
    )
