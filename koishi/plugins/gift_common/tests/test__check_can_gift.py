from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import GuildProfile, User
from hata.ext.slash import InteractionAbortedError

from ....bot_utils.constants import ROLE__SUPPORT__BOOSTER, ROLE__SUPPORT__ELEVATED

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, Relationship

from ..checks import check_can_gift


def _iter_options__passing():
    user_id_0 = 202502230000
    user_id_1 = 202502230001
    user_id_2 = 202502230002
    user_id_3 = 202502230003
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_0 = User.precreate(user_id_0)
    user_2 = User.precreate(user_id_2)
    user_2.guild_profiles[ROLE__SUPPORT__BOOSTER.guild_id] = GuildProfile(role_ids = [ROLE__SUPPORT__BOOSTER.id])
    user_3 = User.precreate(user_id_3)
    user_3.guild_profiles[ROLE__SUPPORT__ELEVATED.guild_id] = GuildProfile(role_ids = [ROLE__SUPPORT__ELEVATED.id])
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1200, now)
    
    # match relationship
    yield (
        user_0,
        relationship_0,
    )
    
    # match booster role
    yield (
        user_2,
        None,
    )
    
    # match orin's workcarrier role
    yield (
        user_3,
        None,
    )


def _iter_options__failing():
    user_id_0 = 202502230004
    
    user_0 = User.precreate(user_id_0)
    
    # no relation / role
    yield (
        user_0,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
def test__check_can_gift(source_user, relationship):
    """
    Tests whether ``check_can_gift`` works as intended.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is gifting.
    
    relationship : `None | Relationship`
        The relationship connecting the two users (can be extend).
    
    Raises
    ------
    InteractionAbortedError
    """
    check_can_gift(source_user, relationship)
