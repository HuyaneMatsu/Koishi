import vampytest
from hata import KOKORO
from scarletio import Future, Task, skip_ready_cycle

from ..constants import RELATIONSHIP_REQUEST_CACHE, RELATIONSHIP_REQUEST_QUERY_TASKS
from ..relationship_request_queries import get_relationship_request
from ..relationship_request import RelationshipRequest
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


async def test__get_relationship_request__cached():
    """
    Tests whether ``get_relationship_request`` works as intended.
    
    Case: cached.
    """
    source_user_id_0 = 202601180040
    target_user_id_0 = 202601180041
    source_user_id_1 = 202601180042
    target_user_id_1 = 202601180043
    
    entry_id_0 = 120
    entry_id_1 = 121
    
    async def mocked_query_relationship_request(user_id, waiters):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_relationship_request,
        query_relationship_request = mocked_query_relationship_request,
    )
    
    try:
        relationship_request_0 = RelationshipRequest(
            source_user_id_0,
            target_user_id_0,
            RELATIONSHIP_TYPE_MAMA,
            1200,
        )
        
        relationship_request_1 = RelationshipRequest(
            source_user_id_1,
            target_user_id_1,
            RELATIONSHIP_TYPE_MAMA,
            1203,
        )
        
        RELATIONSHIP_REQUEST_CACHE[entry_id_0] = relationship_request_0
        RELATIONSHIP_REQUEST_CACHE[entry_id_1] = relationship_request_1
        
        vampytest.assert_eq(
            [*RELATIONSHIP_REQUEST_CACHE.keys()],
            [entry_id_0, entry_id_1],
        )
        
        output = await mocked(entry_id_0)
        vampytest.assert_instance(output, RelationshipRequest)
        vampytest.assert_is(output, relationship_request_0)
        
        vampytest.assert_eq(
            [*RELATIONSHIP_REQUEST_CACHE.keys()],
            [entry_id_0, entry_id_1],
        )
        
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()


async def test__get_relationship_request__request():
    """
    Tests whether ``get_relationship_request`` works as intended.
    
    Case: requesting.
    """
    source_user_id = 202601180045
    target_user_id = 202601180046
    relationship_type = RELATIONSHIP_TYPE_MAMA
    investment = 2000
    
    entry_id = 124
    
    relationship_request = None
    
    entry = {
        'id': entry_id,
        'investment': investment,
        'relationship_type': relationship_type,
        'source_user_id': source_user_id,
        'target_user_id': target_user_id,
    }
    
    async def mocked_query_relationship_request(input_entry_id, waiters):
        nonlocal entry
        nonlocal entry_id
        nonlocal relationship_request
        
        try:
            vampytest.assert_eq(input_entry_id, entry_id)
            vampytest.assert_instance(waiters, list)
            for element in waiters:
                vampytest.assert_instance(element, Future)
            
            relationship_request = RelationshipRequest.from_entry(entry)
            
            RELATIONSHIP_REQUEST_CACHE[entry_id] = relationship_request
            
            for waiter in waiters:
                waiter.set_result_if_pending(relationship_request)
        
        finally:
            try:
                del RELATIONSHIP_REQUEST_QUERY_TASKS[entry_id]
            except KeyError:
                pass
    
    
    mocked = vampytest.mock_globals(
        get_relationship_request,
        query_relationship_request = mocked_query_relationship_request,
        recursion = 2
    )
    
    task_0 = None
    task_1 = None
    
    try:
        task_0 = Task(KOKORO, mocked(entry_id))
        task_0.apply_timeout(0.1)
        task_1 = Task(KOKORO, mocked(entry_id))
        task_1.apply_timeout(0.1)
        
        vampytest.assert_eq(
            [*RELATIONSHIP_REQUEST_CACHE.keys()],
            [],
        )
        
        vampytest.assert_false(RELATIONSHIP_REQUEST_QUERY_TASKS)
        
        await skip_ready_cycle()
        
        vampytest.assert_true(RELATIONSHIP_REQUEST_QUERY_TASKS)
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is_not(relationship_request, None)
        vampytest.assert_is(relationship_request, output_0)
        vampytest.assert_is(relationship_request, output_1)
        
        vampytest.assert_eq(
            [*RELATIONSHIP_REQUEST_CACHE.keys()],
            [entry_id],
        )
        
        vampytest.assert_false(RELATIONSHIP_REQUEST_QUERY_TASKS)
        
    finally:
        RELATIONSHIP_REQUEST_CACHE.clear()
        RELATIONSHIP_REQUEST_QUERY_TASKS.clear()
        
        if (task_0 is not None):
            task_0.cancel()
        
        if (task_1 is not None):
            task_1.cancel()
