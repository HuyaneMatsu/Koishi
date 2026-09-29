from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...quest_core import (
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, quest_create, quest_requirement_instantiable_create_expiration,
    quest_sub_type_instantiable_create_base
)

from ..helpers import get_quest_expiration


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
                quest_requirement_instantiable_create_expiration(DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
            ),
            None,
        ),
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(quest):
    """
    Tests whether ``get_quest_expiration`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = get_quest_expiration(quest)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
