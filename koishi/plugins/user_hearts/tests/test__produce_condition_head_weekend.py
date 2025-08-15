import vampytest
from hata import InteractionEvent, User

from ....bot_utils.daily import ConditionWeekend

from ..rendering import produce_condition_head_weekend


def _iter_options():
    yield (
        ConditionWeekend(),
        InteractionEvent.precreate(
            202412020009,
            user = User.precreate(202412020010),
        ),
        f'**Its weekend:**\n',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_condition_head_weekend(condition, interaction_event):
    """
    Tests whether ``produce_condition_head_weekend`` works as intended.
    
    Parameters
    ----------
    condition : ``ConditionWeekend``
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    return ''.join(produce_condition_head_weekend(condition, interaction_event))
