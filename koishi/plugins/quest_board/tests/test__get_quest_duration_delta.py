import vampytest
from dateutil.relativedelta import relativedelta as RelativeDelta

from ...quest_core import (
    QUEST_TEMPLATE_ID_SAKUYA_STRAWBERRY, quest_create, quest_requirement_instantiable_create_duration,
    quest_sub_type_instantiable_create_base
)

from ..helpers import get_quest_duration_delta


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
                quest_requirement_instantiable_create_duration(3600),
            ),
            None,
        ),
        RelativeDelta(seconds = 3600),
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__get_quest_submission_requirements_normalised(quest):
    """
    Tests whether ``get_quest_duration_delta`` works as intended.
    
    Parameters
    ----------
    quest : ``Quest``
        Quest to work with.
    
    Returns
    -------
    output : `None | RelativeDelta`
    """
    output = get_quest_duration_delta(quest)
    vampytest.assert_instance(output, RelativeDelta, nullable = True)
    return output
