import vampytest

from ..linked_quest import LinkedQuest
from ..quest_reward_serialisables import QuestRewardSerialisableBase, QuestRewardSerialisableCredibility
from ..quest_template_ids import QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
from ..utils import get_linked_quest_abandon_credibility_penalty


def _iter_options():
    quest_template_id = QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY
    
    user_id = 202603130000
    guild_id = 202603130001
    batch_id = 5666
    
    linked_quest_0 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_template_id,
        None,
        None,
    )
    
    yield (
        linked_quest_0,
        4,
        0,
    )
    
    linked_quest_1 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_template_id,
        None,
        (
            QuestRewardSerialisableBase(),
        ),
    )
    
    yield (
        linked_quest_1,
        4,
        0,
    )
    

    linked_quest_2 = LinkedQuest(
        user_id,
        guild_id,
        batch_id,
        quest_template_id,
        None,
        (
            QuestRewardSerialisableCredibility(20),
        ),
    )
    
    yield (
        linked_quest_2,
        4,
        26,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_abandon_credibility_penalty(linked_quest, entity_rank):
    """
    Tests whether ``get_linked_quest_abandon_credibility_penalty`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to get the penalty for.
    
    entity_rank : `int`
        The entity's rank to be rewarded.
    
    Returns
    -------
    output : `int`
    """
    output = get_linked_quest_abandon_credibility_penalty(linked_quest, entity_rank)
    vampytest.assert_instance(output, int)
    return output
