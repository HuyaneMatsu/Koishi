from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError
 
from ...relationships_core import (
    RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_MAMA, RELATIONSHIP_TYPE_MISTRESS, RELATIONSHIP_TYPE_WAIFU, Relationship
)

from ..checks import async_check_target_already_has_mistress


def _iter_options__passing():
    user_id_0 = 202501040020
    user_id_1 = 202501040021
    user_id_2 = 202501040022
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Alice')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        RELATIONSHIP_TYPE_MISTRESS,
        None,
        True,
        user_0,
        user_1,
        0,
        {},
    )
    
    yield (
        RELATIONSHIP_TYPE_MISTRESS,
        None,
        False,
        user_0,
        user_1,
        0,
        {},
    )
    
    yield (
        RELATIONSHIP_TYPE_MISTRESS,
        [
            Relationship(user_id_2, user_id_1, RELATIONSHIP_TYPE_MAMA, 500, now),
        ],
        True,
        user_0,
        user_1,
        0,
        {},
    )
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        [
            Relationship(user_id_2, user_id_1, RELATIONSHIP_TYPE_WAIFU, 500, now),
        ],
        True,
        user_0,
        user_1,
        0,
        {},
    )


def _iter_options__failing():
    user_id_0 = 202501040023
    user_id_1 = 202501040024
    user_id_2 = 202501040025
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Reisen')
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    yield (
        RELATIONSHIP_TYPE_MISTRESS,
        [
            Relationship(user_id_2, user_id_1, RELATIONSHIP_TYPE_MISTRESS, 500, now),
        ],
        True,
        user_0,
        user_1,
        0,
        {
            user_id_2 : user_2,
        }
    )
    yield (
        RELATIONSHIP_TYPE_MISTRESS,
        [
            Relationship(user_id_1, user_id_2, RELATIONSHIP_TYPE_MAID, 500, now),
        ],
        True,
        user_0,
        user_1,
        0,
        {
            user_id_2 : user_2,
        }
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
async def test__async_check_target_already_has_mistress(
    relationship_type,
    target_relationship_listing,
    checked_at_creation,
    source_user,
    target_user,
    guild_id,
    user_request_table,
):
    """
    Tests whether ``async_check_target_already_has_mistress`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
    
    target_relationship_listing : `None | list<Relationship>`
        The relationship_listing of the target user.
    
    checked_at_creation : `bool`
        Whether called from request creation.
    
    source_user : ``ClientUserBase``
        The source user.
    
    target_user : ``ClientUserBase``
        The target user.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    async def mock_get_user(input_user_id):
        nonlocal user_request_table
        user = user_request_table.get(input_user_id, None)
        if user is None:
            raise RuntimeError(input_user_id)
        
        return user
    
    
    mocked = vampytest.mock_globals(
        async_check_target_already_has_mistress,
        get_user = mock_get_user,
    )
    
    await mocked(
        relationship_type, target_relationship_listing, checked_at_creation, source_user, target_user, guild_id
    )
