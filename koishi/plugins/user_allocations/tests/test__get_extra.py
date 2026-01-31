import vampytest
from hata import User

from ...relationships_core import RELATIONSHIP_TYPE_MAMA, RelationshipRequest
from ...user_balance import ALLOCATION_FEATURE_ID_NONE, ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST

from ..extra import get_extra


async def test__get_extra__none():
    """
    Tests whether ``get_extra`` works as intended.
    
    Case: none.
    """
    user_id = 202601180060
    allocation_feature_id = ALLOCATION_FEATURE_ID_NONE
    session_id = 160
    amount = 1000
    session = None
    
    output = await get_extra(user_id, allocation_feature_id, session_id, amount, session)
    vampytest.assert_is(output, None)
    

async def test__get_extra__relationship_request():
    """
    Tests whether ``get_extra`` works as intended.
    
    Case: none.
    """
    user_id_0 = 202601180061
    user_id_1 = 202601180062
    allocation_feature_id = ALLOCATION_FEATURE_ID_RELATIONSHIP_REQUEST
    session_id = 160
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
    
    async def patched_get_relationship_request_entry_extra(
        input_user_id, input_session_id, input_amount, input_session
    ):
        nonlocal user_id_0
        nonlocal session_id
        nonlocal amount
        nonlocal session
        nonlocal user_1
        
        vampytest.assert_eq(input_user_id, user_id_0)
        vampytest.assert_eq(input_session_id, session_id)
        vampytest.assert_eq(input_amount, amount)
        vampytest.assert_eq(input_session, session)
        
        return (user_1,)
    
    
    mocked = vampytest.mock_globals(
        get_extra,
        get_relationship_request_entry_extra = patched_get_relationship_request_entry_extra,
    )    
    
    output = await mocked(user_id_0, allocation_feature_id, session_id, amount, session)
    vampytest.assert_eq(output, (user_1, ))
