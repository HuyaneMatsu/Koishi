import vampytest
from hata import GuildProfile, User
from hata.ext.slash import InteractionAbortedError

from ....bot_utils.constants import MAX_WAIFU_SLOTS

from ..checks import check_max_relationship_slots_other


def _iter_options__passing():
    user_id = 202501260003
    guild_id = 202501260004
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    yield MAX_WAIFU_SLOTS - 1, user, guild_id


def _iter_options__failing():
    user_id = 202501260005
    guild_id = 202501260006
    
    user = User.precreate(user_id, name = 'Keine')
    user.guild_profiles[guild_id] = GuildProfile(nick = 'Caver')
    
    yield MAX_WAIFU_SLOTS, user, guild_id
    yield MAX_WAIFU_SLOTS + 1, user, guild_id


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_max_relationship_slots_other(relationship_slots, user, guild_id):
    """
    Tests whether ``check_max_relationship_slots_other`` works as intended.
    
    Parameters
    ----------
    relationship_slots : `int`
        The amount of relationship slots.
    
    user : `ClientUserBase``
        The targeted user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    check_max_relationship_slots_other(relationship_slots, user, guild_id)
