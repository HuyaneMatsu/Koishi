from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..constants import RELATIONSHIP_LISTING_CACHE, RELATIONSHIP_LISTING_GET_QUERY_TASKS
from ..relationship import Relationship
from ..relationship_queries import get_relationship_listing
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


async def test__get_relationship_listing__in_cache():
    """
    Tests whether ``get_relationship_listing`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    """
    async def mock_query_relationship_listing(input_user_id):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_relationship_listing,
        query_relationship_listing = mock_query_relationship_listing,
    )
    
    source_user_id_0 = 202501020070
    target_user_id_0 = 202501020071
    source_user_id_1 = 202501020072
    target_user_id_1 = 202501020073
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship_0 = Relationship(
        source_user_id_0,
        target_user_id_0,
        RELATIONSHIP_TYPE_MAMA,
        1200,
        now,
    )
    
    relationship_1 = Relationship(
        source_user_id_1,
        target_user_id_1,
        RELATIONSHIP_TYPE_MAMA,
        1203,
        now,
    )
    try:
        RELATIONSHIP_LISTING_CACHE[source_user_id_0] = [relationship_0]
        RELATIONSHIP_LISTING_CACHE[source_user_id_1] = [relationship_1]
        
        output = await mocked(source_user_id_0)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, [relationship_0])
        
        vampytest.assert_eq(
            [*RELATIONSHIP_LISTING_CACHE.items()],
            [
                (source_user_id_1, [relationship_1]),
                (source_user_id_0, [relationship_0]),
            ],
        )
    finally:
        RELATIONSHIP_LISTING_CACHE.clear()


async def test__get_relationship_listing__query():
    """
    Tests whether ``get_relationship_listing`` works as intended.
    
    Case: query.
    
    This function is a coroutine.
    """
    async def mock_query_relationship_listing(input_user_id):
        nonlocal source_user_id
        nonlocal relationship
        
        vampytest.assert_eq(input_user_id, source_user_id)
        
        return [relationship]
    
    
    mocked = vampytest.mock_globals(
        get_relationship_listing,
        query_relationship_listing = mock_query_relationship_listing,
    )
    
    source_user_id = 202501020074
    target_user_id = 202501020075
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship = Relationship(
        source_user_id,
        target_user_id,
        RELATIONSHIP_TYPE_MAMA,
        1200,
        now,
    )
    
    try:
        output = await mocked(source_user_id)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, [relationship])
        
        vampytest.assert_eq(
            [*RELATIONSHIP_LISTING_CACHE.items()],
            [
                (source_user_id, [relationship]),
            ],
        )
    finally:
        RELATIONSHIP_LISTING_CACHE.clear()


async def test__get_relationship_listing__double_query():
    """
    Tests whether ``get_relationship_listing`` works as intended.
    
    Case: double query.
    
    This function is a coroutine.
    """
    async def mock_query_relationship_listing(input_user_id):
        nonlocal source_user_id
        nonlocal relationship
        
        await skip_ready_cycle()
        vampytest.assert_eq(input_user_id, source_user_id)
        
        return [relationship]
    
    
    mocked = vampytest.mock_globals(
        get_relationship_listing,
        query_relationship_listing = mock_query_relationship_listing,
    )
    
    source_user_id = 202501020074
    target_user_id = 202501020075
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship = Relationship(
        source_user_id,
        target_user_id,
        RELATIONSHIP_TYPE_MAMA,
        1200,
        now,
    )
    
    event_loop = get_event_loop()
    
    try:
        task_0 = Task(event_loop, mocked(source_user_id))
        task_1 = Task(event_loop, mocked(source_user_id))
        
        await skip_ready_cycle()
        vampytest.assert_eq(len(RELATIONSHIP_LISTING_GET_QUERY_TASKS), 1)
        
        output_0 = await task_0
        output_1 = await task_1
        
        vampytest.assert_is(output_0, output_1)
        
        vampytest.assert_instance(output_0, list, nullable = True)
        vampytest.assert_eq(output_0, [relationship])
        
        vampytest.assert_eq(
            [*RELATIONSHIP_LISTING_CACHE.items()],
            [
                (source_user_id, [relationship]),
            ],
        )
        
        vampytest.assert_eq(len(RELATIONSHIP_LISTING_GET_QUERY_TASKS), 0)
        
    finally:
        RELATIONSHIP_LISTING_CACHE.clear()
