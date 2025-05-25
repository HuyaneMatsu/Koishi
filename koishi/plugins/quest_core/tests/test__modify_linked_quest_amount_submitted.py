import vampytest

from ..constants import LINKED_QUEST_LISTING_CACHE
from ..linked_quest import LinkedQuest
from ..queries import modify_linked_quest_amount_submitted

from .test__get_linked_quest_listing import _create_test_quest


async def test__modify_linked_quest_amount_submitted__in_cache():
    """
    Tests whether ``modify_linked_quest_amount_submitted`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    """
    query_called = False
    
    async def mock_query_modify_linked_quest_amount_submitted(input_entry_id, input_amount):
        nonlocal entry_id_0
        nonlocal query_called
        nonlocal amount
        
        vampytest.assert_eq(input_entry_id, entry_id_0)
        vampytest.assert_eq(input_amount, amount)
        query_called = True
    
    mocked = vampytest.mock_globals(
        modify_linked_quest_amount_submitted,
        query_modify_lined_quest_amount_submitted = mock_query_modify_linked_quest_amount_submitted,
    )
    
    quest_0 = _create_test_quest()
    user_id_0 = 202505190010
    guild_id_0 = 202505190011
    batch_id_0 = 5666
    entry_id_0 = 130
    
    quest_1 = _create_test_quest()
    user_id_1 = 202505190012
    guild_id_1 = 202505190013
    batch_id_1 = 5666
    entry_id_1 = 131
    
    linked_quest_0 = LinkedQuest(
        user_id_0,
        guild_id_0,
        batch_id_0,
        quest_0,
    )
    linked_quest_0.entry_id = entry_id_0
    
    linked_quest_1 = LinkedQuest(
        user_id_1,
        guild_id_1,
        batch_id_1,
        quest_1,
    )
    linked_quest_1.entry_id = entry_id_1
    
    amount = 12
    
    try:
        LINKED_QUEST_LISTING_CACHE[user_id_0] = [linked_quest_0]
        LINKED_QUEST_LISTING_CACHE[user_id_1] = [linked_quest_1]
        
        await mocked(linked_quest_0, amount)
        
        vampytest.assert_eq(linked_quest_0.amount_submitted, amount)
        
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
