from datetime import datetime as DateTime, timezone as TimeZone 

import vampytest
from hata import Component, User, create_text_display
 
from ...relationships_core import RELATIONSHIP_TYPE_WAIFU, RELATIONSHIP_TYPE_MAMA, Relationship

from ..checks import async_check_target_already_has_waifu


def _iter_options():
    user_id_0 = 202501040010
    user_id_1 = 202501040011
    user_id_2 = 202501040012
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Alice')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        None,
        True,
        user_1,
        0,
        {},
        None,
    )
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        None,
        True,
        user_1,
        0,
        {},
        None,
    )
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        [
            Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_MAMA, 500, now),
        ],
        True,
        user_1,
        0,
        {},
        None,
    )
    
    yield (
        RELATIONSHIP_TYPE_MAMA,
        [
            Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_MAMA, 500, now),
        ],
        True,
        user_1,
        0,
        {},
        None,
    )
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        [
            Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_WAIFU, 500, now),
        ],
        True,
        user_1,
        0,
        {
            user_id_2 : user_2,
        },
        [
            create_text_display(
                'Koishi is already married to Alice!'
            ),
        ],
    )
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        [
            Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_WAIFU, 500, now),
        ],
        False,
        user_1,
        0,
        {
            user_id_2 : user_2,
        },
        [
            create_text_display(
                'You are already married to Alice!'
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__async_check_target_already_has_waifu(
    relationship_type, target_relationship_listing, checked_at_creation, target_user, guild_id, user_request_table
):
    """
    Tests whether ``async_check_target_already_has_waifu`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
    
    target_relationship_listing : `None | list<Relationship>`
        The relationship_listing of the target user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``None | list<Component>``
    """
    async def mock_get_user(input_user_id):
        nonlocal user_request_table
        user = user_request_table.get(input_user_id, None)
        if user is None:
            raise RuntimeError(input_user_id)
        
        return user
    
    
    mocked = vampytest.mock_globals(
        async_check_target_already_has_waifu,
        get_user = mock_get_user,
    )
    
    output = await mocked(
        relationship_type, target_relationship_listing, checked_at_creation, target_user, guild_id
    )
    
    vampytest.assert_instance(output, list, nullable = True)
    
    if (output is not None):
        for element in output:
            vampytest.assert_instance(element, Component, nullable = True)
    
    return output
