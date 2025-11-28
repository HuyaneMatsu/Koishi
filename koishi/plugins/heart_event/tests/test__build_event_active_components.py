from datetime import timedelta as TimeDelta

import vampytest
from hata import Component, create_button, create_row, create_text_display

from ....bot_utils.constants import EMOJI__HEART_CURRENCY

from ..component_building import build_event_active_components
from ..constants import EVENT_MODE_STREAK


def _iter_options():
    yield (
        EVENT_MODE_STREAK,
        TimeDelta(days = 1),
        10,
        333,
        None,
        True,
        [
            create_text_display(
                f'Click the {EMOJI__HEART_CURRENCY} button to receive 10 streak.\n'
                f'1 days left or 333 uses.'
            ),
            create_row(
                create_button(
                    custom_id = 'heart_event.active',
                    emoji = EMOJI__HEART_CURRENCY,
                    enabled = True,
                ),
            ),
        ],
    )
    
    yield (
        EVENT_MODE_STREAK,
        TimeDelta(days = 1),
        10,
        0,
        None,
        False,
        [
            create_text_display(
                f'Click the {EMOJI__HEART_CURRENCY} button to receive 10 streak.\n'
                f'1 days left.'
            ),
            create_row(
                create_button(
                    custom_id = 'heart_event.inactive',
                    emoji = EMOJI__HEART_CURRENCY,
                    enabled = False,
                ),
            ),
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_event_active_components(event_mode, duration, amount, user_limit, user_ids, active):
    """
    Tests whether ``build_event_active_components`` works as intended.
    
    Parameters
    ---------
    event_mode : `int`
        The event's mode.
    
    duration : `TimeDelta`
        Event duration.
    
    amount : `int`
        Reward amount.
    
    user_limit : `int`
        The maximal amount of users allowed to receive reward.
    
    active : `bool`
        Whether the event is active.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_event_active_components(event_mode, duration, amount, user_limit, user_ids, active)
    
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    
    return output
