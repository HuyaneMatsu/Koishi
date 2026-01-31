from datetime import datetime as DateTime, timezone as TimeZone

import vampytest
from hata import KOKORO
from scarletio import Task, skip_ready_cycle

from ..constants import RELATIONSHIP_SAVE_TASKS
from ..relationship import Relationship
from ..relationship_queries import save_relationship
from ..relationship_types import RELATIONSHIP_TYPE_SISTER_LIL


async def test__save_relationship__cached():
    """
    Tests whether ``save_relationship`` works as intended.
    
    Case: cached.
    """
    user_id_0 = 202601140010
    user_id_1 = 202601140011
    
    now = DateTime(2016, 5, 14, tzinfo = TimeZone.utc)
    
    async def patched_query_save_relationship_loop(input_relationship):
        nonlocal relationship
        vampytest.assert_is(input_relationship, relationship)
        await skip_ready_cycle()
    
    
    mocked = vampytest.mock_globals(
        save_relationship,
        query_save_relationship_loop = patched_query_save_relationship_loop,
    )
    
    
    relationship = Relationship(user_id_0, user_id_1, RELATIONSHIP_TYPE_SISTER_LIL, 2000, now)
    
    try:
        task = Task(KOKORO, mocked(relationship))
        await skip_ready_cycle()
        vampytest.assert_in((user_id_0, user_id_1), RELATIONSHIP_SAVE_TASKS)
        await task
        vampytest.assert_is(relationship.modified_fields, None)
        
    finally:
        RELATIONSHIP_SAVE_TASKS.clear()
