import vampytest

from ..linked_quest import LinkedQuest, linked_quest_create
from ..quest_reward_serialisables import QuestRewardSerialisableBase, QuestRewardSerialisableCredibility
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
from ..utils import get_linked_quest_abandon_credibility_penalty


def _iter_options():
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    user_id = 202603130000
    guild_id = 202603130001
    batch_id = 5666
    current_unix_time_seconds = 10000
    
    linked_quest_0 = linked_quest_create(
        user_id,
        guild_id,
        batch_id,
        quest_template_id,
        None,
        None,
    )
    linked_quest_0.created_at = 5000
    
    yield (
        linked_quest_0,
        4,
        current_unix_time_seconds,
        0,
    )
    
    
    linked_quest_1 = linked_quest_create(
        user_id,
        guild_id,
        batch_id,
        quest_template_id,
        None,
        (
            QuestRewardSerialisableBase(),
        ),
    )
    linked_quest_1.created_at = 5000
    
    yield (
        linked_quest_1,
        4,
        current_unix_time_seconds,
        0,
    )
    

    linked_quest_2 = linked_quest_create(
        user_id,
        guild_id,
        batch_id,
        quest_template_id,
        None,
        (
            QuestRewardSerialisableCredibility(20),
        ),
    )
    linked_quest_2.created_at = 5000
    
    yield (
        linked_quest_2,
        4,
        current_unix_time_seconds,
        26,
    )
    

    linked_quest_2 = linked_quest_create(
        user_id,
        guild_id,
        batch_id,
        quest_template_id,
        None,
        (
            QuestRewardSerialisableCredibility(20),
        ),
    )
    linked_quest_2.created_at = current_unix_time_seconds
    
    yield (
        linked_quest_2,
        4,
        current_unix_time_seconds,
        0,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_abandon_credibility_penalty(linked_quest, entity_rank, current_unix_time_seconds):
    """
    Tests whether ``get_linked_quest_abandon_credibility_penalty`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to get the penalty for.
    
    entity_rank : `int`
        The entity's rank to be rewarded.
    
    current_unix_time_seconds : `int`
        The current unix time.
    
    Returns
    -------
    output : `int`
    """
    def unix_time_seconds_get():
        nonlocal current_unix_time_seconds
        return current_unix_time_seconds
    
    mocked = vampytest.mock_globals(
        get_linked_quest_abandon_credibility_penalty,
        unix_time_seconds_get = unix_time_seconds_get,
    )
    
    output = mocked(linked_quest, entity_rank)
    vampytest.assert_instance(output, int)
    return output
