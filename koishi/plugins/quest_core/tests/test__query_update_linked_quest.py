import vampytest

from ..constants import LINKED_QUEST_LISTING_CACHE
from ..linked_quest import LinkedQuest
from ..queries import update_linked_quest

from .helpers import _create_linked_quest_additional_input_fields


async def test__update_linked_quest__in_cache():
    """
    Tests whether ``update_linked_quest`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    """
    query_called = False
    
    async def mock_query_update_linked_quest(input_linked_quest):
        nonlocal linked_quest_0
        nonlocal query_called
        vampytest.assert_is(input_linked_quest, linked_quest_0)
        query_called = True
    
    mocked = vampytest.mock_globals(
        update_linked_quest,
        query_update_linked_quest = mock_query_update_linked_quest,
    )
    
    user_id_0 = 202505190010
    guild_id_0 = 202505190011
    batch_id_0 = 5666
    entry_id_0 = 130
    additional_input_fields_0 = _create_linked_quest_additional_input_fields()
    
    user_id_1 = 202505190012
    guild_id_1 = 202505190013
    batch_id_1 = 5666
    entry_id_1 = 131
    additional_input_fields_1 = _create_linked_quest_additional_input_fields()
    
    linked_quest_0 = LinkedQuest(
        user_id_0,
        guild_id_0,
        batch_id_0,
        *additional_input_fields_0,
    )
    linked_quest_0.entry_id = entry_id_0
    
    linked_quest_1 = LinkedQuest(
        user_id_1,
        guild_id_1,
        batch_id_1,
        *additional_input_fields_1,
    )
    linked_quest_1.entry_id = entry_id_1
    
    try:
        LINKED_QUEST_LISTING_CACHE[user_id_0] = [linked_quest_0]
        LINKED_QUEST_LISTING_CACHE[user_id_1] = [linked_quest_1]
        
        await mocked(linked_quest_0)
        
        
        # This does not affect cache position.
        vampytest.assert_eq(
            [*LINKED_QUEST_LISTING_CACHE.items()],
            [
                (user_id_0, [linked_quest_0]),
                (user_id_1, [linked_quest_1]),
            ],
        )
        vampytest.assert_true(query_called)
    
    finally:
        LINKED_QUEST_LISTING_CACHE.clear()
