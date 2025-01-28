import vampytest

from ..constants import RELATIONSHIP_REQUEST_CACHE_LISTING
from ..relationship_request import RelationshipRequest
from ..relationship_request_queries import get_relationship_request_listing
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


async def test__get_relationship_request_listing__in_cache():
    """
    Tests whether ``get_relationship_request_listing`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    """
    async def mock_query_relationship_request_listing(input_user_id, input_outgoing):
        raise RuntimeError
    
    
    mocked = vampytest.mock_globals(
        get_relationship_request_listing,
        query_relationship_request_listing = mock_query_relationship_request_listing,
    )
    
    outgoing = True
    source_user_id_0 = 202412270030
    target_user_id_0 = 202412270031
    source_user_id_1 = 202412270032
    target_user_id_1 = 202412270033
    
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
    try:
        RELATIONSHIP_REQUEST_CACHE_LISTING[source_user_id_0, True] = [relationship_request_0]
        RELATIONSHIP_REQUEST_CACHE_LISTING[source_user_id_1, True] = [relationship_request_1]
        
        output = await mocked(source_user_id_0, outgoing)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, [relationship_request_0])
        
        vampytest.assert_eq(
            [*RELATIONSHIP_REQUEST_CACHE_LISTING.items()],
            [
                ((source_user_id_1, True), [relationship_request_1]),
                ((source_user_id_0, True), [relationship_request_0]),
            ],
        )
    finally:
        RELATIONSHIP_REQUEST_CACHE_LISTING.clear()


async def test__get_relationship_request_listing__query():
    """
    Tests whether ``get_relationship_request_listing`` works as intended.
    
    Case: query.
    
    This function is a coroutine.
    """
    async def mock_query_relationship_request_listing(input_user_id, input_outgoing):
        nonlocal outgoing
        nonlocal source_user_id
        nonlocal relationship_request
        
        vampytest.assert_eq(input_outgoing, outgoing)
        vampytest.assert_eq(input_user_id, source_user_id)
        
        return [relationship_request]
    
    
    mocked = vampytest.mock_globals(
        get_relationship_request_listing,
        query_relationship_request_listing = mock_query_relationship_request_listing,
    )
    
    outgoing = True
    source_user_id = 202412270034
    target_user_id = 202412270035
    
    relationship_request = RelationshipRequest(
        source_user_id,
        target_user_id,
        RELATIONSHIP_TYPE_MAMA,
        1200,
    )
    
    try:
        output = await mocked(source_user_id, outgoing)
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, [relationship_request])
        
        vampytest.assert_eq(
            [*RELATIONSHIP_REQUEST_CACHE_LISTING.items()],
            [
                ((source_user_id, True), [relationship_request]),
            ],
        )
    finally:
        RELATIONSHIP_REQUEST_CACHE_LISTING.clear()
