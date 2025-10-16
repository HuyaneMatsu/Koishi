import vampytest
from scarletio import Task, get_event_loop, skip_ready_cycle

from ..constants import LINKED_QUEST_LISTING_CACHE, LINKED_QUEST_LISTING_GET_QUERY_TASKS
from ..linked_quest import LinkedQuest
from ..linked_quest_completion_states import LINKED_QUEST_COMPLETION_STATE_COMPLETED
from ..queries import get_linked_quest_listing
from ..quest import Quest
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY


def _create_test_quest():
    duration = 3600 * 24 * 3
    amount = 4
    reward_balance = 2600
    reward_credibility = 4
    template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    return Quest(
        template_id,
        amount,
        duration,
        reward_credibility,
        reward_balance,
    )


async def test__get_linked_quest_listing__in_cache():
    """
    Tests whether ``get_linked_quest_listing`` works as intended.
    
    Case: in cache.
    
    This function is a coroutine.
    """
    current_batch_id = 5666
    query_delete_linked_quests_called = False
    
    async def mock_query_linked_quest_listing(input_user_id):
        raise RuntimeError
    
    async def mock_query_delete_linked_quests(entry_ids):
        nonlocal entry_id_2
        nonlocal query_delete_linked_quests_called
        
        vampytest.assert_eq(entry_ids, [entry_id_2])
        query_delete_linked_quests_called = True
    
    def mock_get_current_batch_id():
        nonlocal current_batch_id
        return current_batch_id
    
    mocked = vampytest.mock_globals(
        get_linked_quest_listing,
        query_linked_quest_listing = mock_query_linked_quest_listing,
        query_delete_linked_quests = mock_query_delete_linked_quests,
        get_current_batch_id = mock_get_current_batch_id,
        recursion = 2,
    )
    
    quest_0 = _create_test_quest()
    user_id_0 = 202505190000
    guild_id_0 = 202505190001
    batch_id_0 = current_batch_id
    entry_id_0 = 122
    
    quest_1 = _create_test_quest()
    user_id_1 = 202505190002
    guild_id_1 = 202505190003
    batch_id_1 = current_batch_id
    entry_id_1 = 123
    
    quest_2 = _create_test_quest()
    guild_id_2 = 202510120001
    batch_id_2 = 5665
    entry_id_2 = 124
    
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
    
    linked_quest_2 = LinkedQuest(
        user_id_0,
        guild_id_2,
        batch_id_2,
        quest_2,
    )
    linked_quest_2.entry_id = entry_id_2
    linked_quest_2.completion_count = 1
    linked_quest_2.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    event_loop = get_event_loop()
    
    try:
        LINKED_QUEST_LISTING_CACHE[user_id_0] = [linked_quest_0, linked_quest_2]
        LINKED_QUEST_LISTING_CACHE[user_id_1] = [linked_quest_1]
        
        task = Task(event_loop, mocked(user_id_0))
        task.apply_timeout(0.1)
        output = await task
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, [linked_quest_0])
        
        vampytest.assert_eq(
            [*LINKED_QUEST_LISTING_CACHE.items()],
            [
                (user_id_1, [linked_quest_1]),
                (user_id_0, [linked_quest_0]),
            ],
        )
        
        vampytest.assert_true(query_delete_linked_quests_called)
    finally:
        LINKED_QUEST_LISTING_CACHE.clear()


async def test__get_linked_quest_listing__query():
    """
    Tests whether ``get_linked_quest_listing`` works as intended.
    
    Case: query.
    
    This function is a coroutine.
    """
    current_batch_id = 5666
    query_delete_linked_quests_called = False
    
    async def mock_query_linked_quest_listing(input_user_id):
        nonlocal user_id_0
        nonlocal linked_quest_0
        nonlocal linked_quest_2
        
        vampytest.assert_eq(input_user_id, user_id_0)
        
        return [linked_quest_0, linked_quest_2]
    
    async def mock_query_delete_linked_quests(entry_ids):
        nonlocal entry_id_2
        nonlocal query_delete_linked_quests_called
        
        vampytest.assert_eq(entry_ids, [entry_id_2])
        query_delete_linked_quests_called = True
    
    def mock_get_current_batch_id():
        nonlocal current_batch_id
        return current_batch_id
    
    
    mocked = vampytest.mock_globals(
        get_linked_quest_listing,
        query_linked_quest_listing = mock_query_linked_quest_listing,
        query_delete_linked_quests = mock_query_delete_linked_quests,
        get_current_batch_id = mock_get_current_batch_id,
        recursion = 3,
    )
    
    quest_0 = _create_test_quest()
    user_id_0 = 202505190004
    guild_id_0 = 202505190005
    batch_id_0 = current_batch_id
    entry_id_0 = 124
    
    quest_2 = _create_test_quest()
    guild_id_2 = 202510120002
    batch_id_2 = 5665
    entry_id_2 = 124
    
    linked_quest_0 = LinkedQuest(
        user_id_0,
        guild_id_0,
        batch_id_0,
        quest_0,
    )
    linked_quest_0.entry_id = entry_id_0
    
    linked_quest_2 = LinkedQuest(
        user_id_0,
        guild_id_2,
        batch_id_2,
        quest_2,
    )
    linked_quest_2.entry_id = entry_id_2
    linked_quest_2.completion_count = 1
    linked_quest_2.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    event_loop = get_event_loop()
    
    try:
        task = Task(event_loop, mocked(user_id_0))
        task.apply_timeout(0.1)
        output = await task
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_instance(output, list, nullable = True)
        vampytest.assert_eq(output, [linked_quest_0])
        
        vampytest.assert_eq(
            [*LINKED_QUEST_LISTING_CACHE.items()],
            [
                (user_id_0, [linked_quest_0]),
            ],
        )
        
        vampytest.assert_true(query_delete_linked_quests_called)
    finally:
        LINKED_QUEST_LISTING_CACHE.clear()


async def test__get_linked_quest_listing__double_query():
    """
    Tests whether ``get_linked_quest_listing`` works as intended.
    
    Case: double query.
    
    This function is a coroutine.
    """
    current_batch_id = 5666
    query_delete_linked_quests_called = False
    
    async def mock_query_linked_quest_listing(input_user_id):
        nonlocal user_id_0
        nonlocal linked_quest_0
        
        await skip_ready_cycle()
        vampytest.assert_eq(input_user_id, user_id_0)
        
        return [linked_quest_0]
    
    
    async def mock_query_delete_linked_quests(entry_ids):
        nonlocal query_delete_linked_quests_called
        query_delete_linked_quests_called = True
        raise RuntimeError()
    
    
    def mock_get_current_batch_id():
        nonlocal current_batch_id
        return current_batch_id
    
    
    mocked = vampytest.mock_globals(
        get_linked_quest_listing,
        query_linked_quest_listing = mock_query_linked_quest_listing,
        query_delete_linked_quests = mock_query_delete_linked_quests,
        get_current_batch_id = mock_get_current_batch_id,
        recursion = 3,
    )
    
    quest_0 = _create_test_quest()
    user_id_0 = 202505190006
    guild_id_0 = 202505190007
    batch_id_0 = current_batch_id
    entry_id_0 = 125
    
    linked_quest_0 = LinkedQuest(
        user_id_0,
        guild_id_0,
        batch_id_0,
        quest_0,
    )
    linked_quest_0.entry_id = entry_id_0
    
    event_loop = get_event_loop()
    
    try:
        task_0 = Task(event_loop, mocked(user_id_0))
        task_1 = Task(event_loop, mocked(user_id_0))
        
        task_0.apply_timeout(0.1)
        task_1.apply_timeout(0.1)
        
        await skip_ready_cycle()
        
        vampytest.assert_eq(len(LINKED_QUEST_LISTING_GET_QUERY_TASKS), 1)
        
        output_0 = await task_0
        output_1 = await task_1
        
        await skip_ready_cycle()
        await skip_ready_cycle()
        
        vampytest.assert_is(output_0, output_1)
        
        vampytest.assert_instance(output_0, list, nullable = True)
        vampytest.assert_eq(output_0, [linked_quest_0])
        
        vampytest.assert_eq(
            [*LINKED_QUEST_LISTING_CACHE.items()],
            [
                (user_id_0, [linked_quest_0]),
            ],
        )
        
        vampytest.assert_eq(len(LINKED_QUEST_LISTING_GET_QUERY_TASKS), 0)
        
        vampytest.assert_false(query_delete_linked_quests_called)
    finally:
        LINKED_QUEST_LISTING_CACHE.clear()
