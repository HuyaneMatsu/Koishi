from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import GuildProfile, User

from ....bot_utils.constants import ROLE__SUPPORT__BOOSTER, ROLE__SUPPORT__ELEVATED

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, Relationship

from ..utils import can_gift_with_request


def _iter_options():
    user_id_0 = 202502240010
    user_id_1 = 202502240011
    user_id_2 = 202502240012
    user_id_3 = 202502240013
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    user_2.guild_profiles[ROLE__SUPPORT__BOOSTER.guild_id] = GuildProfile(role_ids = [ROLE__SUPPORT__BOOSTER.id])
    user_3 = User.precreate(user_id_3)
    user_3.guild_profiles[ROLE__SUPPORT__ELEVATED.guild_id] = GuildProfile(role_ids = [ROLE__SUPPORT__ELEVATED.id])
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1200, now)
    
    # match relationship
    yield (
        user_0,
        user_1,
        relationship_0,
        True,
    )
    
    # match booster role
    yield (
        user_2,
        user_1,
        None,
        True,
    )
    
    # match orin's workcarrier role
    yield (
        user_3,
        user_1,
        None,
        True,
    )
    
    # no relation / role
    yield (
        user_0,
        user_1,
        None,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__can_gift_with_request(source_user, target_user, get_relationship_to_deepen_return):
    """
    Tests whether ``can_gift_with_request`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is gifting.
    
    target_user : ``ClientUserBase``
        The gifted user.
    
    get_relationship_to_deepen_return : `None | Relationship`
        Return of the mocked ``get_relationship_to_deepen`` function.
    
    Raises
    ------
    InteractionAbortedError
    """
    async def mocked_get_relationship_to_deepen(passed_source_user_id, passed_target_user_id):
        nonlocal source_user
        nonlocal target_user
        nonlocal get_relationship_to_deepen_return
        
        
        return get_relationship_to_deepen_return
    
    mocked = vampytest.mock_globals(
        can_gift_with_request,
        get_relationship_to_deepen = mocked_get_relationship_to_deepen,
    )
    
    output = await mocked(source_user, target_user)
    vampytest.assert_instance(output, bool)
    return output
