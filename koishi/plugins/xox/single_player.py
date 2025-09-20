__all__ = ()

from functools import partial as partial_func
from random import random

from hata import Client, DiscordException, ERROR_CODES
from hata.ext.slash import iter_component_interactions

from .ai import click_ai
from .constants import (
    GAME_STATE_DRAW, GAME_STATE_NONE, GAME_STATE_P1_WIN, PLAYER_SETTINGS_KOISHI, PLAYER_SETTINGS_SATORI
)
from .helpers import check_event_user, click, get_game_state
from .renderers import render_components



async def xox_single_player(client, event):
    """
    The X-O-X game against ai.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    array = [0 for _ in range(9)]
    
    if random() < 0.5:
        player_settings_user = PLAYER_SETTINGS_KOISHI
        player_settings_ai = PLAYER_SETTINGS_SATORI
    else:
        player_settings_user = PLAYER_SETTINGS_SATORI
        player_settings_ai = PLAYER_SETTINGS_KOISHI
    
    if random() < 0.5:
        click_ai(array, player_settings_ai.identifier, player_settings_user.identifier)
    
    title = f'It is your turn {event.user.full_name} | {player_settings_user.emoji.as_emoji}'
    
    await client.interaction_response_message_create(
        event,
        title,
        components = render_components(array, False, player_settings_user, player_settings_ai),
    )
    
    component_interaction_event = None
    
    try:
        async for component_interaction_event in iter_component_interactions(
            event, timeout = 300.0, check = partial_func(check_event_user, event.user)
        ):
            
            if not click(array, component_interaction_event.custom_id, player_settings_user.identifier):
                await client.interaction_component_acknowledge(component_interaction_event)
                continue
            
            game_state = get_game_state(array, player_settings_user.identifier)
            if game_state == GAME_STATE_NONE:
                click_ai(array, player_settings_ai.identifier, player_settings_user.identifier)
                game_state = get_game_state(array, player_settings_user.identifier)
                if game_state == GAME_STATE_NONE:
                    await client.interaction_component_message_edit(
                        component_interaction_event,
                        components = render_components(array, False, player_settings_user, player_settings_ai),
                    )
                    continue
            
            if game_state == GAME_STATE_DRAW:
                title = 'Draw'
            elif game_state == GAME_STATE_P1_WIN:
                title = 'You won'
            else:
                title = f'{client.full_name} won'
            
            await client.interaction_component_message_edit(
                component_interaction_event,
                title,
                components = render_components(array, True, player_settings_user, player_settings_ai),
            )
            break
    
    except TimeoutError:
        title = 'Timeout occurred.'
        
        try:
            await client.interaction_response_message_edit(
                event if (component_interaction_event is None) else component_interaction_event,
                title,
                components = render_components(array, True, player_settings_user, player_settings_ai)
            )
        except DiscordException as err:
            if err.code not in (
                ERROR_CODES.unknown_message,
            ):
                raise
