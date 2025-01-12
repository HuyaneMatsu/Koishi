import vampytest

from ..relationship_request import RelationshipRequest
from ..relationship_request_completion import _iter_relationship_request_user_ids_to_request
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_BIG


def _iter_options():
    user_id_0 = 20250109010
    user_id_1 = 20250109011
    user_id_2 = 20250109012
    user_id_3 = 20250109013
    
    relationship_0 = RelationshipRequest(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_BIG, 2000)
    relationship_1 = RelationshipRequest(user_id_2, user_id_0, RELATIONSHIP_TYPE_SISTER_BIG, 2000)
    relationship_2 = RelationshipRequest(user_id_0, user_id_3, RELATIONSHIP_TYPE_SISTER_BIG, 2000)
    
    yield (
        True,
        [relationship_0, relationship_2],
        [user_id_1, user_id_3],
    )
    yield (
        False,
        [relationship_1],
        [user_id_2],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__iter_relationship_request_user_ids_to_request(outgoing, relationships):
    """
    Tests whether ``_iter_relationship_request_user_ids_to_request`` works as intended.
    
    Parameters
    ----------
    outgoing : `bool`
        Whether to auto complete the outgoing users.
    
    relationship_requests : `list<RelationshipRequest>`
        The relationship requests to get the user identifiers from.
    
    Returns
    -------
    output : `list<int>`
    """
    output = sorted(_iter_relationship_request_user_ids_to_request(outgoing, relationships))
    
    for element in output:
        vampytest.assert_instance(element, int)
    
    return output
