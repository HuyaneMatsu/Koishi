from datetime import datetime as DateTime, timezone as TimeZone

import vampytest

from ...quest_core import (
    LinkedQuest, QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, QuestRequirementSerialisableBase,
    QuestRequirementSerialisableExpiration
)

from ..helpers import get_linked_quest_expiration


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
                QuestRequirementSerialisableExpiration(DateTime(2016, 5, 14, tzinfo = TimeZone.utc)),
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
