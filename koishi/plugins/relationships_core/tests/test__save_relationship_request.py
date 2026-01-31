import vampytest
from hata import KOKORO
from scarletio import Task, skip_ready_cycle

from ..constants import RELATIONSHIP_REQUEST_SAVE_TASKS
from ..relationship_request import RelationshipRequest
from ..relationship_request_queries import save_relationship_request
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_LIL


async def test__save_relationship_request__cached():
    """
    Tests whether ``save_relationship_request`` works as intended.
    
    Case: cached.
    """
    user_id_0 = 202601140010
    user_id_1 = 202601140011
    
    async def patched_query_save_relationship_request_loop(input_relationship_request):
        nonlocal relationship_request
        vampytest.assert_is(input_relationship_request, relationship_request)
        await skip_ready_cycle()
    
    
    mocked = vampytest.mock_globals(
        save_relationship_request,
        query_save_relationship_request_loop = patched_query_save_relationship_request_loop,
    )
    
    
    relationship_request = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_LIL, 2000)
    
    try:
        task = Task(KOKORO, mocked(relationship_request))
        await skip_ready_cycle()
        vampytest.assert_in((user_id_0, user_id_1), RELATIONSHIP_REQUEST_SAVE_TASKS)
        await task
        vampytest.assert_is(relationship_request.modified_fields, None)
        
    finally:
        RELATIONSHIP_REQUEST_SAVE_TASKS.clear()
