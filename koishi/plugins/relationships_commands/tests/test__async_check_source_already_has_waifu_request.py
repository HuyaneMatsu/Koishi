import vampytest
from hata import User
from hata.ext.slash import InteractionAbortedError

from ...relationships_core import RELATIONSHIP_TYPE_WAIFU, RELATIONSHIP_TYPE_MAMA, RelationshipRequest

from ..checks import async_check_source_already_has_waifu_request


def _iter_options__passing():
    user_id_0 = 202501040000
    user_id_1 = 202501040001
    user_id_2 = 202501040002
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Alice')
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        None,
        user_1,
        0,
        {},
    )
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        [
            RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 500),
        ],
        user_1,
        0,
        {},
    )


def _iter_options__failing():
    user_id_0 = 202501040003
    user_id_1 = 202501040004
    user_id_2 = 202501040005
    
    user_0 = User.precreate(user_id_0, name = 'Satori')
    user_1 = User.precreate(user_id_1, name = 'Koishi')
    user_2 = User.precreate(user_id_2, name = 'Reisen')
    
    yield (
        RELATIONSHIP_TYPE_WAIFU,
        [
            RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_WAIFU, 500),
        ],
        user_1,
        0,
        {
            user_id_2 : user_2,
        }
    )


@vampytest._(vampytest.call_from(_iter_options__passing()))
@vampytest._(vampytest.call_from(_iter_options__failing()).raising(InteractionAbortedError))
async def test__async_check_source_already_has_waifu_request(
    relationship_type, source_relationship_request_listing, target_user, guild_id, user_request_table
):
    """
    Tests whether ``async_check_source_already_has_waifu_request`` works as intended.
    
    Parameters
    ----------
    relationship_type : `int`
        The requested relationship type.
    
    source_relationship_request_listing : `None | list<RelationshipRequest>`
        The relationship requests of the source user.
    
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
            raise RuntimeError
        
        return user
    
    
    mocked = vampytest.mock_globals(
        async_check_source_already_has_waifu_request,
        get_user = mock_get_user,
    )
    
    await mocked(
        relationship_type, source_relationship_request_listing, target_user, guild_id
    )
