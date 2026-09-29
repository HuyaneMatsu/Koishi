import vampytest

from ...item_core import ITEM_GROUP_ID_KNIFE, ITEM_ID_STRAWBERRY
from ...quest_core import (
    LINKED_QUEST_COMPLETION_STATE_COMPLETED, linked_quest_create, QUEST_REQUIREMENT_TYPE_ITEM_EXACT,
    QUEST_REQUIREMENT_TYPE_ITEM_GROUP, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, quest_sub_type_serialisable_create_base,
    quest_requirement_serialisable_create_item_exact, quest_requirement_serialisable_create_item_group
)
from ...unit_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT

from ..helpers import get_linked_quest_submission_requirements_normalised


def _iter_options():
    yield (
        linked_quest_create(
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
        linked_quest_create(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_sub_type_serialisable_create_base(),
            ),
            None,
        ),
        None,
    )
    
    yield (
        linked_quest_create(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
                quest_requirement_serialisable_create_item_group(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, 0),
            ),
            None,
        ),
        [
            (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
            (QUEST_REQUIREMENT_TYPE_ITEM_GROUP, ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, 0),
        ],
    )
    
    yield (
        linked_quest_create(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
                quest_sub_type_serialisable_create_base(),
            ),
            None,
        ),
        [
            (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 200),
        ],
    )
    
    linked_quest = linked_quest_create(
        0,
        0,
        0,
        QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
        (
            quest_requirement_serialisable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, 560),
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
