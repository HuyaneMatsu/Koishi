from datetime import timedelta as TimeDelta

import vampytest
from hata import InteractionForm, create_text_display

from ..component_building import build_event_confirmation_form
from ..constants import EVENT_MODE_STREAK


def _iter_options():
    yield (
        EVENT_MODE_STREAK,
        TimeDelta(days = 1),
        10,
        333,
        InteractionForm(
            'Please confirm the event.',
            [
                create_text_display(
                    'Duration : 1 days\n'
                    'Amount : 10\n'
                    'User limit : 333'
                ),
            ],
            custom_id = f'heart_event.new.{EVENT_MODE_STREAK:x}.{86400:x}.{10:x}.{333:x}',
        )
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_event_confirmation_form(event_mode, duration, amount, user_limit):
    """
    Tests whether ``build_event_confirmation_form`` works as intended.
    
    Parameters
    ----------
    event_mode : `int`
        The event's mode.
    
    duration : `TimeDelta`
        Event duration.
    
    amount : `int`
        Reward amount.
    
    user_limit : `int`
        The maximal amount of users allowed to receive reward.
    
    Returns
    -------
    output : ``InteractionForm``
    """
    output = build_event_confirmation_form(event_mode, duration, amount, user_limit)
    vampytest.assert_instance(output, InteractionForm)
    return output
