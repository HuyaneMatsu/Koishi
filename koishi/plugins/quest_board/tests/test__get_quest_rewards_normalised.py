import vampytest

from ...item_core import ITEM_ID_STRAWBERRY
from ...quest_core import (
    QUEST_REWARD_TYPE_CREDIBILITY, QUEST_REWARD_TYPE_ITEM_EXACT, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, Quest,
    QuestRewardInstantiableBase, QuestRewardInstantiableCredibility, QuestRewardInstantiableItemExact
)

from ..helpers import get_quest_rewards_normalised


def _iter_options():
    yield (
        Quest(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            None,
        ),
        0,
        0,
        None,
    )
    
    yield (
        Quest(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardInstantiableBase(),
            ),
        ),
        0,
        0,
        None,
    )
    
    yield (
        Quest(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardInstantiableItemExact(ITEM_ID_STRAWBERRY, 100),
                QuestRewardInstantiableCredibility(20),
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
        Quest(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardInstantiableItemExact(ITEM_ID_STRAWBERRY, 500),
                QuestRewardInstantiableBase(),
            ),
        ),
        0,
        4,
        [
            (QUEST_REWARD_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, 500),
        ],
    )
    
    yield (
        Quest(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            (
                QuestRewardInstantiableCredibility(20),
            ),
        ),
        0,
        3,
        [
            (QUEST_REWARD_TYPE_CREDIBILITY, 0, 10),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_rewards_normalised(quest, quest_level, user_level):
    """
    Tests whether ``get_quest_rewards_normalised`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    quest_level : `int`
        The quest's level.
    
    user_level : `int`
        The user's level.
    
    Returns
    -------
    output : `None | list<(int, int, int)>`
    """
    output = get_quest_rewards_normalised(quest, quest_level, user_level)
    vampytest.assert_instance(output, list, nullable = True)
    return output
