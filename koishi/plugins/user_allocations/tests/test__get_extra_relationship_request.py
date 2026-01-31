import vampytest
from hata import ClientUserBase, User

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, RelationshipRequest

from ..extra_relationship_request import get_relationship_request_entry_extra


async def test__get_relationship_request_entry_extra__no_session():
    """
    Tests whether ``get_relationship_request_entry_extra`` works as intended.
    
    This function is a coroutine.
    """
    user_id_0 = 202601180050
    user_id_1 = 202601180051
    
    session_id = 123
    amount = 1000
    session = None
    
    async def patched_get_user(input_user_id):
        raise RuntimeError('Unexpected request')
    
    mocked = vampytest.mock_globals(
        get_relationship_request_entry_extra,
        get_user = patched_get_user,
    )
    
    output = await mocked(user_id_0, session_id, amount, session)
    vampytest.assert_instance(output, tuple, nullable = True)
    vampytest.assert_is(output, None)
    

async def test__get_relationship_request_entry_extra__with_session():
    """
    Tests whether ``get_relationship_request_entry_extra`` works as intended.
    
    This function is a coroutine.
    """
    user_id_0 = 202601180052
    user_id_1 = 202601180053
    
    session_id = 123
    amount = 1000
    session = RelationshipRequest(
        user_id_0,
        user_id_1,
        RELATIONSHIP_TYPE_MAMA,
        1000,
    )
    session.entry_id = session_id
    
    user_1 = User.precreate(
        user_id_1,
    )
    
    async def patched_get_user(input_user_id):
        nonlocal user_id_1
        nonlocal user_1
        vampytest.assert_eq(input_user_id, user_id_1)
        return user_1
    
    mocked = vampytest.mock_globals(
        get_relationship_request_entry_extra,
        get_user = patched_get_user,
    )
    
    output = await mocked(user_id_0, session_id, amount, session)
    vampytest.assert_instance(output, tuple, nullable = True)
    vampytest.assert_eq(output, (user_1, ))
