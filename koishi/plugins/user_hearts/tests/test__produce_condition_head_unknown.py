import vampytest
from hata import InteractionEvent, User

from ....bot_utils.daily import ConditionBase

from ..rendering import produce_condition_head_unknown


def _iter_options():
    yield (
        ConditionBase(),
        InteractionEvent.precreate(
            202412020013,
            user = User.precreate(202412020014),
        ),
        f'**Unknown:**\n',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_condition_head_unknown(condition, interaction_event):
    """
    Tests whether ``produce_condition_head_unknown`` works as intended.
    
    Parameters
    ----------
    condition : ``ConditionBase``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    return ''.join(produce_condition_head_unknown(condition, interaction_event))
