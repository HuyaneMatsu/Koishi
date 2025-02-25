from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import GuildProfile, User

from ....bot_utils.constants import ROLE__SUPPORT__BOOSTER, ROLE__SUPPORT__ELEVATED

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, Relationship

from ..utils import can_gift


def _iter_options():
    user_id_0 = 202502240010
    user_id_1 = 202502240011
    user_id_2 = 202502240012
    user_id_3 = 202502240013
    
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
        True,
    )
    
    # match booster role
    yield (
        user_2,
        None,
        True,
    )
    
    # match orin's workcarrier role
    yield (
        user_3,
        None,
        True,
    )
    
    # no relation / role
    yield (
        user_0,
        None,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__can_gift(source_user, relationship):
    """
    Tests whether ``can_gift`` works as intended.
    
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
    output = can_gift(source_user, relationship)
    vampytest.assert_instance(output, bool)
    return output
