import vampytest

from ...item_core import ITEM_ID_STRAWBERRY
from ...quest_core import (
    QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_ITEM_EXACT, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, LinkedQuest,
    QuestRewardSerialisableBase, QuestRewardSerialisableCredibility, QuestRewardSerialisableItemExact
)

from ..helpers import get_linked_quest_rewards_normalised


def _iter_options():
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            None,
        ),
        0,
        0,
        None,
    )
    
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableBase(),
            ),
        ),
        0,
        0,
        None,
    )
    
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableItemExact(ITEM_ID_STRAWBERRY, 100),
                QuestRewardSerialisableCredibility(20),
            ),
        ),
        0,
        0,
        [
            (QUEST_REWARD_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, 100),
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 20),
        ],
    )
    
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableItemExact(ITEM_ID_STRAWBERRY, 500),
                QuestRewardSerialisableBase(),
            ),
        ),
        0,
        4,
        [
            (QUEST_REWARD_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, 500),
        ],
    )
    
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardSerialisableCredibility(20),
            ),
        ),
        0,
        3,
        [
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 10),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_rewards_normalised(linked_quest, quest_level, user_level):
    """
    Tests whether ``get_linked_quest_rewards_normalised`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    quest_level : `int`
        The quest's level.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    output : `None | list<(int, int, int)>`
    """
    output = get_linked_quest_rewards_normalised(linked_quest, quest_level, user_level)
    vampytest.assert_instance(output, list, nullable = True)
    return output
