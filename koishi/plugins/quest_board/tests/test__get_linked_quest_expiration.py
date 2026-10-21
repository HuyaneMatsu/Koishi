import vampytest

from ...quest_core import (
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, linked_quest_create, quest_requirement_serialisable_create_expiration,
    quest_sub_type_serialisable_create_base
)

from ..constants import EXPIRATION_DEFAULT
from ..helpers import get_linked_quest_expiration


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
        EXPIRATION_DEFAULT,
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
        EXPIRATION_DEFAULT,
    )
    
    yield (
        linked_quest_create(
            0,
            0,
            0,
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_requirement_serialisable_create_expiration(1000000),
            ),
            None,
        ),
        1000000,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(linked_quest):
    output = get_linked_quest_expiration(linked_quest)
    vampytest.assert_instance(output, int)
    return output
