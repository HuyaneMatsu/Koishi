import vampytest
from dateutil.relativedelta import relativedelta as RelativeDelta

from ...quest_core import (
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, LinkedQuest, QuestRequirementInstantiableBase,
    QuestRequirementInstantiableDuration
)

from ..helpers import get_linked_quest_duration_delta


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
                QuestRequirementInstantiableBase(),
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
                QuestRequirementInstantiableDuration(3600),
            ),
            None,
        ),
        RelativeDelta(seconds = 3600),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(quest):
    """
    Tests whether ``get_linked_quest_duration_delta`` works as intended.
    
    Parameters
    ----------
    quest : ``LinkedQuest``
        LinkedQuest to work with.
    
    Returns
    -------
    output : `None | RelativeDelta`
    """
    output = get_linked_quest_duration_delta(quest)
    vampytest.assert_instance(output, RelativeDelta, nullable = True)
    return output
