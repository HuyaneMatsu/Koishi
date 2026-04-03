__all__ = ()

from hata import InteractionForm, create_button, create_row, create_text_display

from ...bot_utils.constants import EMOJI__HEART_CURRENCY

from .constants import EVENT_MODE_HEART, EVENT_MODE_STREAK
from .custom_ids import CUSTOM_ID_EVENT_ACTIVE, CUSTOM_ID_EVENT_CONFIRMATION_FACTORY, CUSTOM_ID_EVENT_INACTIVE
from .helpers import produce_time_delta


def _produce_event_confirmation_form_description(duration, amount, user_limit):
    """
    Helper function to produce event confirmation form.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    duration : `TimeDelta`
        Event duration.
    
    amount : `int`
        Reward amount.
    
    user_limit : `int`
        The maximal amount of users allowed to receive reward.
    
    Yields
    ------
    part : `str`
    """
    yield 'Duration : '
    yield from produce_time_delta(duration)
    
    yield '\nAmount : '
    yield str(amount)
    
    if user_limit:
        yield '\nUser limit : '
        yield str(user_limit)


def build_event_confirmation_form(event_mode, duration, amount, user_limit):
    """
    builds event confirmation form.
    
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
    form : ``InteractionForm``
    """
    return InteractionForm(
        'Please confirm the event.',
        [
            create_text_display(''.join([*_produce_event_confirmation_form_description(
                duration, amount, user_limit
            )])),
        ],
        custom_id = CUSTOM_ID_EVENT_CONFIRMATION_FACTORY(event_mode, duration, amount, user_limit),
    )


def _produce_event_active_description(event_mode, duration, amount, user_limit, user_ids):
    """
    Produces active event description.
    
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
    
    Yields
    ------
    part : `str`
    """
    yield 'Click the '
    yield EMOJI__HEART_CURRENCY.as_emoji
    yield ' button to receive '
    yield str(amount)
    yield ' '
    
    if event_mode == EVENT_MODE_HEART:
        name = 'hearts'
    elif event_mode == EVENT_MODE_STREAK:
        name = 'streak'
    else:
        name = 'unknown'
    yield name
    yield '.\n'
    
    yield from produce_time_delta(duration)
    yield ' left'
    
    if user_limit:
        yield ' or '
        yield str(user_limit - (0 if user_ids is None else len(user_ids)))
        yield ' uses'
    
    yield '.'


def build_event_active_components(event_mode, duration, amount, user_limit, user_ids, active):
    """
    Builds event active components.
    
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
    components : ``list<Component>``
    """
    return [
        create_text_display(''.join([*_produce_event_active_description(
            event_mode, duration, amount, user_limit, user_ids
        )])),
        create_row(
            create_button(
                custom_id = (CUSTOM_ID_EVENT_ACTIVE if active else CUSTOM_ID_EVENT_INACTIVE),
                emoji = EMOJI__HEART_CURRENCY,
                enabled = active,
            ),
        ),
    ]
