import vampytest

from ...quest_core import (
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, linked_quest_create, quest_requirement_instantiable_create_duration,
    quest_sub_type_instantiable_create_base
)

from ..helpers import get_linked_quest_duration


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
        0,
    )
    
    yield (
        linked_quest_create(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_sub_type_instantiable_create_base(),
            ),
            None,
        ),
        0,
    )
    
    yield (
        linked_quest_create(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_requirement_instantiable_create_duration(3600),
            ),
            None,
        ),
        3600,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(quest):
    output = get_linked_quest_duration(quest)
    vampytest.assert_instance(output, int)
    return output
