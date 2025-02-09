import vampytest

from hata import ClientUserBase
from hata.ext.slash import InteractionAbortedError

from ..relationship_request import RelationshipRequest
from ..relationship_request_completion import get_relationship_request
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    user_id_0 = 202502070010
    user_id_1 = 202502070011
    user_id_2 = 202502070012
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        user_id_2,
        [
            relationship_request_0,
            relationship_request_1,
        ],
        relationship_request_1,
    )


def _iter_options__aborted():
    user_id_0 = 202502070013
    user_id_1 = 202502070014
    user_id_2 = 202502070015
    
    yield (
        user_id_0,
        user_id_2,
        None,
    )
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    
    yield (
        user_id_0,
        user_id_2,
        [
            relationship_request_0,
        ],
    )
    

@vampytest._(vampytest.call_from(_iter_options()).returning_last())
@vampytest._(vampytest.call_from(_iter_options__aborted()).raising(InteractionAbortedError))
async def test__get_relationship_request(source_user_id, target_user_id, relationship_requests):
    """
    Tests whether ``get_relationship_request`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user_id : `int`
        Source user identifier to get relationships for.
    
    target_user_id : `int`
        The target user's identifier.
    
    relationship_requests : `None | list<RelationshipRequest>`
        Relationship requests to return when requested.
    
    Returns
    -------
    output : `RelationshipRequest`
    
    Raises
    ------
    InteractionAbortedError
    """
    async def mock_get_relationship_request_listing(input_user_id, input_outgoing):
        nonlocal target_user_id
        nonlocal source_user_id
        nonlocal relationship_requests
        
        vampytest.assert_in((input_user_id, input_outgoing), ((source_user_id, True), (source_user_id, False)))
        return relationship_requests
    
    mocked = vampytest.mock_globals(
        get_relationship_request,
        get_relationship_request_listing = mock_get_relationship_request_listing,
    )
    
    output = await mocked(source_user_id, target_user_id)
    vampytest.assert_instance(output, RelationshipRequest)
    return output
