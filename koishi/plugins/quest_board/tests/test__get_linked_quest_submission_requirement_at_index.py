import vampytest

from ...item_core import ITEM_GROUP_ID_KNIFE, ITEM_ID_STRAWBERRY
from ...quest_core import (
    AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT, LinkedQuest, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
    QuestRequirementSerialisableBase, QuestRequirementSerialisableItemExact, QuestRequirementSerialisableItemGroup
)

from ..helpers import get_linked_quest_submission_requirement_at_index


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
        0,
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
        0,
        QuestRequirementSerialisableItemExact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
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
        1,
        QuestRequirementSerialisableItemGroup(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, 0),
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
        2,
        None,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_linked_quest_submission_requirement_at_index(linked_quest, requirement_index):
    """
    Tests whether ``get_linked_quest_submission_requirement_at_index`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    requirement_index : `int`
        The index of the submission requirement.
    
    Returns
    -------
    output : ``None | QuestRequirementSerialisableBase``
    """
    output = get_linked_quest_submission_requirement_at_index(linked_quest, requirement_index)
    vampytest.assert_instance(output, QuestRequirementSerialisableBase, nullable = True)
    return output
