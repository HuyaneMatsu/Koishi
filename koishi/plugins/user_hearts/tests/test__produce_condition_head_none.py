import vampytest
from hata import InteractionEvent, User

from ..rendering import produce_condition_head_none


def _iter_options():
    yield (
        None,
        InteractionEvent.precreate(
            202412020000,
            user = User.precreate(202412020001),
        ),
        '**Base:**\n',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_condition_head_none(condition, interaction_event):
    """
    Tests whether ``produce_condition_head_none`` works as intended.
    
    Parameters
    ----------
    condition : `None`
        Condition to produce.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    output : `str`
    """
    return ''.join(produce_condition_head_none(condition, interaction_event))
