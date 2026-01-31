from collections import OrderedDict

import vampytest
from scarletio import WeakValueDictionary

from ....bot_utils.models import DB_ENGINE

from ..relationship_request import RelationshipRequest
from ..relationship_request_queries import delete_relationship_request
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_LIL


@vampytest.skip_if(DB_ENGINE is not None)
async def test__delete_relationship_request():
    """
    Tests whether ``delete_relationship_request`` works as intended.
    
    This function is a coroutine.
    """
    user_id_0 = 202601160000
    user_id_1 = 202601160001
    
    relationship_request = RelationshipRequest(
        user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_LIL, 2000
    )
    
    entry_id = 133
    relationship_request.entry_id = entry_id
    
    relationship_request_cache_patched = WeakValueDictionary()
    relationship_request_cache_patched[entry_id] = relationship_request
    relationship_request_listing_cache_patched = OrderedDict()
    relationship_request_listing_cache_patched[(user_id_0, True)] = [relationship_request]
    
    mocked = vampytest.mock_globals(
        delete_relationship_request,
        2,
        RELATIONSHIP_REQUEST_CACHE = relationship_request_cache_patched,
        RELATIONSHIP_REQUEST_LISTING_CACHE = relationship_request_listing_cache_patched,
    )
    
    await mocked(relationship_request)
    
    vampytest.assert_eq(
        {*relationship_request_cache_patched.keys()},
        set(),
    )
    
    vampytest.assert_eq(
        [*relationship_request_listing_cache_patched.items()],
        [((user_id_0, True), None)],
    )
