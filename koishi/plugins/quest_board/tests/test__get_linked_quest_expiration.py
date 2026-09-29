from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...quest_core import (
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, linked_quest_create, quest_requirement_serialisable_create_expiration,
    quest_sub_type_serialisable_create_base
)

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
                quest_requirement_serialisable_create_expiration(DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
            ),
            None,
        ),
        DateTime(2016, 5, 14, tzinfo = TimeZone.utc),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(linked_quest):
    """
    Tests whether ``get_linked_quest_expiration`` works as intended.
    
    Parameters
    ----------
    linked_quest : ``LinkedQuest``
        Linked quest to work with.
    
    Returns
    -------
    output : `None | DateTime`
    """
    output = get_linked_quest_expiration(linked_quest)
    vampytest.assert_instance(output, DateTime, nullable = True)
    return output
