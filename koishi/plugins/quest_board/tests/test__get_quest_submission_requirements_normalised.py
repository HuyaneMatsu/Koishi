import vampytest

from ...item_core import ITEM_GROUP_ID_KNIFE, ITEM_ID_STRAWBERRY
from ...quest_core import (
    QUEST_REQUIREMENT_TYPE_ITEM_EXACT, QUEST_REQUIREMENT_TYPE_ITEM_GROUP,
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, quest_create, quest_requirement_instantiable_create_item_exact,
    quest_requirement_instantiable_create_item_group, quest_sub_type_instantiable_create_base
)
from ...unit_core import AMOUNT_TYPE_COUNT, AMOUNT_TYPE_WEIGHT

from ..helpers import get_quest_submission_requirements_normalised


def _iter_options():
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            None,
        ),
        None,
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_sub_type_instantiable_create_base(),
            ),
            None,
        ),
        None,
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_requirement_instantiable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500),
                quest_requirement_instantiable_create_item_group(ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1),
            ),
            None,
        ),
        [
            (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, -1),
            (QUEST_REQUIREMENT_TYPE_ITEM_GROUP, ITEM_GROUP_ID_KNIFE, AMOUNT_TYPE_COUNT, 1, -1),
        ],
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_requirement_instantiable_create_item_exact(ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500),
                quest_sub_type_instantiable_create_base(),
            ),
            None,
        ),
        [
            (QUEST_REQUIREMENT_TYPE_ITEM_EXACT, ITEM_ID_STRAWBERRY, AMOUNT_TYPE_WEIGHT, 500, -1),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(quest):
    """
    Tests whether ``get_quest_submission_requirements_normalised`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    Returns
    -------
    output : `None | list<(int, int, int, int, int)>`
    """
    output = get_quest_submission_requirements_normalised(quest)
    vampytest.assert_instance(output, list, nullable = True)
    return output
