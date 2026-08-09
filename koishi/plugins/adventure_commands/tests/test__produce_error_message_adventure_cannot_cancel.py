import vampytest

from ...adventure_core import (
    ADVENTURE_STATE_ACTIONING_CANCEL_AFTER, ADVENTURE_STATE_CANCELLED, ADVENTURE_STATE_FINALIZED,
    ADVENTURE_STATE_RETURNING

)
from ..constants import (
    ADVENTURE_CANCELLATION_MODE_AFTER, ADVENTURE_CANCELLATION_MODE_NONE, ADVENTURE_CANCELLATION_MODE_NOW
)
from ..content_building import produce_error_message_adventure_cannot_cancel


def _iter_options():
    yield (
        ADVENTURE_STATE_CANCELLED,
        ADVENTURE_CANCELLATION_MODE_NOW,
        'You cannot cancel your adventure immediately while you are returning home.'
    )
    
    yield (
        ADVENTURE_STATE_RETURNING,
        ADVENTURE_CANCELLATION_MODE_NOW,
        'You cannot cancel your adventure immediately while you are returning home.'
    )
    
    yield (
        ADVENTURE_STATE_ACTIONING_CANCEL_AFTER,
        ADVENTURE_CANCELLATION_MODE_AFTER,
        'You cannot cancel your adventure after the next action if it is already being cancelled after the next action.'
    )
    
    yield (
        ADVENTURE_STATE_CANCELLED,
        ADVENTURE_CANCELLATION_MODE_AFTER,
        'You cannot cancel your adventure after the next action while you are returning home.'
    )
    
    yield (
        ADVENTURE_STATE_RETURNING,
        ADVENTURE_CANCELLATION_MODE_AFTER,
        'You cannot cancel your adventure after the next action while you are returning home.'
    )
    
    yield (
        ADVENTURE_STATE_FINALIZED,
        ADVENTURE_CANCELLATION_MODE_NONE,
        'You cannot cancel your adventure.'
    )
    
    yield (
        ADVENTURE_STATE_CANCELLED,
        ADVENTURE_CANCELLATION_MODE_NONE,
        'You cannot cancel your adventure while you are returning home.'
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__produce_error_message_adventure_cannot_cancel(adventure_state, cancellation_mode):
    """
    Tests whether ``produce_error_message_adventure_cannot_cancel`` works as intended.
    
    Parameters
    ----------
    adventure_state : `int`
        The adventure's state.
    
    cancellation_mode : `int`
        Cancellation mode.
    
    Returns
    -------
    output : `str`
    """
    output = [*produce_error_message_adventure_cannot_cancel(adventure_state, cancellation_mode)]
    
    for element in output:
        vampytest.assert_instance(element, str)
    
    return ''.join(output)
