import vampytest

from ..relationship_request import RelationshipRequest
from ..relationship_request_completion import get_relationship_request_from
from ..relationship_types import RELATIONSHIP_TYPE_MAMA


def _iter_options():
    user_id_0 = 202601170010
    user_id_1 = 202601170011
    user_id_2 = 202601170012
    
    entry_id_0 = 120
    entry_id_1 = 121
    
    relationship_request_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_0.entry_id = entry_id_0
    relationship_request_1 = RelationshipRequest(user_id_0, user_id_2, RELATIONSHIP_TYPE_MAMA, 1000)
    relationship_request_1.entry_id = entry_id_1
    
    yield (
        user_id_0,
        True,
        entry_id_1,
        [
            relationship_request_0,
            relationship_request_1,
        ],
        relationship_request_1,
    )
    
    yield (
        user_id_0,
        True,
        entry_id_1,
        None,
        None,
    )
    
    yield (
        user_id_0,
        True,
        entry_id_1,
        [
            relationship_request_0,
        ],
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
async def test__get_relationship_request_from(user_id, outgoing, entry_id, relationship_requests):
    """
    Tests whether ``get_relationship_request_from`` works as intended.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who is requesting.
    
    outgoing : `bool`
        Whether to auto complete the outgoing users.
    
    entry_id : `int`
        The entry's identifier to get.
    
    relationship_requests : `None | list<RelationshipRequest>`
        Relationship requests to return when requested.
    
    Returns
    -------
    output : ``None | RelationshipRequest``
    """
    async def mock_get_relationship_request_listing(input_user_id, input_outgoing):
        nonlocal user_id
        nonlocal outgoing
        nonlocal relationship_requests
        
        vampytest.assert_eq(input_user_id, user_id)
        vampytest.assert_eq(input_outgoing, outgoing)
        return relationship_requests
    
    mocked = vampytest.mock_globals(
        get_relationship_request_from,
        get_relationship_request_listing = mock_get_relationship_request_listing,
    )
    
    output = await mocked(user_id, outgoing, entry_id)
    vampytest.assert_instance(output, RelationshipRequest, nullable = True)
    return output
