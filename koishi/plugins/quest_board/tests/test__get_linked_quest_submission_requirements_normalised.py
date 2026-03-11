import vampytest

from ...item_core import ITEM_GROUP_ID_KNIFE, ITEM_ID_STRAWBERRY
from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, LINKED_QUEST_COMPLETION_STATE_COMPLETED, LinkedQuest,
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
    QuestRequirementSerialisableBase, QuestRequirementSerialisableItemExact, QuestRequirementSerialisableItemGroup
)

from ..helpers import get_linked_quest_submission_requirements_normalised


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
        None,
    )
    
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                QuestRequirementSerialisableBase(),
            ),
            None,
        ),
        None,
    )
    
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
                QuestRequirementSerialisableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, 0),
            ),
            None,
        ),
        [
            (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
            (QUEST_REQUIREMENT_TYPE_ITEM_GROUP, ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, 0),
        ],
    )
    
    yield (
        LinkedQuest(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
                QuestRequirementSerialisableBase(),
            ),
            None,
        ),
        [
            (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
        ],
    )
    
    linked_quest = LinkedQuest(
        0,
        0,
        0,
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        (
            QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 560),
        ),
        None,
    )
    linked_quest.completion_state = LINKED_QUEST_COMPLETION_STATE_COMPLETED
    
    yield (
        linked_quest,
        [
            (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, -1),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_submission_requirements_normalised(linked_quest):
    """
    Tests whether ``get_linked_quest_submission_requirements_normalised`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    Returns
    -------
    output : `None | list<(int, int, int, int, int)>`
    """
    output = get_linked_quest_submission_requirements_normalised(linked_quest)
    vampytest.assert_instance(output, list, nullable = True)
    return output
