from collections import OrderedDict
from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from scarletio import WeakValueDictionary

from ....bot_utils.models import DB_ENGINE

from ..relationship import Relationship
from ..relationship_queries import delete_relationship
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_LIL


@vampytest.skip_if(DB_ENGINE is not None)
async def test__delete_relationship():
    """
    Tests whether ``delete_relationship`` works as intended.
    
    This function is a coroutine.
    """
    user_id_0 = 202601150000
    user_id_1 = 202601150001
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    relationship = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    
    entry_id = 133
    relationship.entry_id = entry_id
    
    relationship_cache_patched = WeakValueDictionary()
    relationship_cache_patched[entry_id] = relationship
    relationship_listing_cache_patched = OrderedDict()
    relationship_listing_cache_patched[user_id_0] = [relationship]
    
    mocked = vampytest.mock_globals(
        delete_relationship,
        2,
        RELATIONSHIP_CACHE = relationship_cache_patched,
        RELATIONSHIP_LISTING_CACHE = relationship_listing_cache_patched,
    )
    
    await mocked(relationship)
    
    vampytest.assert_eq(
        {*relationship_cache_patched.keys()},
        set(),
    )
    
    vampytest.assert_eq(
        [*relationship_listing_cache_patched.items()],
        [(user_id_0, None)],
    )
