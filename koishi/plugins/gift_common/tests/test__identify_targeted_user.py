from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import ClientUserBase, User

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, Relationship

from ..utils import identify_targeted_user


def _iter_options():
    user_id_0 = 202502240000
    user_id_1 = 202502240001
    user_id_2 = 202502240002
    guild_id = 2025022400023
    
    user_0 = User.precreate(user_id_0)
    user_1 = User.precreate(user_id_1)
    user_2 = User.precreate(user_id_2)
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    # same users.
    yield (
        user_0,
        None,
        user_0,
        guild_id,
        None,
        (
            None,
            None,
            None,
        ),
        (
            None,
            None,
        ),
    )
    
    # target user given | no relationship to deepen
    yield (
        user_0,
        None,
        user_1,
        guild_id,
        None,
        (
            None,
            None,
            None,
        ),
        (
            user_1,
            None,
        ),
    )
    
    # target user given | with relationship to deepen
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1200, now)
    
    yield (
        user_0,
        None,
        user_1,
        guild_id,
        relationship_0,
        (
            None,
            None,
            None,
        ),
        (
            user_1,
            relationship_0,
        ),
    )
    
    # related user name | not related
    
    yield (
        user_0,
        'koishi',
        None,
        guild_id,
        None,
        (
            None,
            None,
            None,
        ),
        (
            None,
            None,
        ),
    )
    
    # related user name | related direct
    
    relationship_0 = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1200, now)
    
    yield (
        user_0,
        'koishi',
        None,
        guild_id,
        None,
        (
            None,
            relationship_0,
            user_1,
        ),
        (
            user_1,
            relationship_0,
        ),
    )
    
    # related user name | related indirect
    
    relationship_0 = Relationship(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1200, now)
    relationship_1 = Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_MAMA, 1200, now)
    
    yield (
        user_0,
        'koishi',
        None,
        guild_id,
        None,
        (
            relationship_0,
            relationship_1,
            user_1,
        ),
        (
            user_1,
            relationship_0,
        ),
    )
    
    # nothing given
    
    yield (
        user_0,
        None,
        None,
        guild_id,
        None,
        (
            None,
            None,
            None,
        ),
        (
            None,
            None
        ),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__identify_targeted_user(
    source_user,
    target_related_name,
    target_user,
    guild_id,
    get_relationship_to_deepen_return,
    get_extender_relationship_and_relationship_and_user_like_at_return,
):
    """
    Tests whether ``identify_targeted_user`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user : ``ClientUserBase``
        The user who is identifying the target user.
    
    target_related_name : `None | str`
        The targeted related user's name.
    
    target_user : `None | ClientUserBase``
        The targeted user's name.
    
    guild_id : `int`
        The targeted guild's name.
    
    get_relationship_to_deepen_return : `None | Relationship`
        Return from `get_relationship_to_deepen_return` call.
    
    get_extender_relationship_and_relationship_and_user_like_at_return : \
            `(None | Relationship, None | Relationship, None | ClientUserBase)`
        Return from `get_extender_relationship_and_relationship_and_user_like_at_return` call.
        
    Returns
    -------
    output : `(None | ClientUserBase, None | Relationship)`
    """
    async def mocked_get_relationship_to_deepen(passed_source_user_id, passed_target_user_id):
        nonlocal source_user
        nonlocal target_user
        nonlocal get_relationship_to_deepen_return
        
        vampytest.assert_is_not(target_user, None)
        vampytest.assert_eq(source_user.id, passed_source_user_id)
        vampytest.assert_eq(target_user.id, passed_target_user_id)
        
        return get_relationship_to_deepen_return
    
    
    async def mocked_get_extender_relationship_and_relationship_and_user_like_at(
        passed_source_user_id, passed_target_related_name, passed_guild_id
    ):
        nonlocal source_user
        nonlocal target_related_name
        nonlocal guild_id
        nonlocal get_extender_relationship_and_relationship_and_user_like_at_return
        
        vampytest.assert_eq(source_user.id, passed_source_user_id)
        vampytest.assert_eq(target_related_name, passed_target_related_name)
        vampytest.assert_eq(guild_id, passed_guild_id)
        return get_extender_relationship_and_relationship_and_user_like_at_return
    
    mocked = vampytest.mock_globals(
        identify_targeted_user,
        get_relationship_to_deepen = mocked_get_relationship_to_deepen,
        get_extender_relationship_and_relationship_and_user_like_at = mocked_get_extender_relationship_and_relationship_and_user_like_at,
    )
    
    output = await mocked(source_user, target_related_name, target_user, guild_id)
    
    vampytest.assert_instance(output, tuple)
    vampytest.assert_eq(len(output), 2)
    vampytest.assert_instance(output[0], ClientUserBase, nullable = True)
    vampytest.assert_instance(output[1], Relationship, nullable = True)
    
    return output
