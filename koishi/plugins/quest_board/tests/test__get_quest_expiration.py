import vampytest

from ...quest_core import (
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, quest_create, quest_requirement_instantiable_create_expiration,
    quest_sub_type_instantiable_create_base
)

from ..constants import EXPIRATION_DEFAULT
from ..helpers import get_quest_expiration


def _iter_options():
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            None,
            None,
        ),
        EXPIRATION_DEFAULT,
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_sub_type_instantiable_create_base(),
            ),
            None,
        ),
        EXPIRATION_DEFAULT,
    )
    
    yield (
        quest_create(
            QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY,
            (
                quest_requirement_instantiable_create_expiration(1000000),
            ),
            None,
        ),
        1000000,
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(quest):
    output = get_quest_expiration(quest)
    vampytest.assert_instance(output, int)
    return output
