__all__ = ()

from functools import partial as partial_func
from random import random

from hata import Client, DiscordException, ERROR_CODES, Embed, KOKORO, create_button
from hata.ext.slash import wait_for_component_interaction
from scarletio import Task

from .constants import (
    BUTTON_CHALLENGE_DISABLED, BUTTON_CHALLENGE_ENABLED, GAME_STATE_DRAW, GAME_STATE_NONE, GAME_STATE_P1_WIN,
    PLAYER_SETTINGS_KOISHI, PLAYER_SETTINGS_SATORI
)
from .helpers import check_event_other_user, check_event_user, click, get_game_state
from .renderers import render_components


async def try_send_notification(client, event, message, user_1, user_2, timestamp, emoji):
    """
    Tries to send to send a notification to the challenged user.
    
    This method is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    message : ``Message``
        The game's target message.
    user_1 : ``ClientUserBase``
        The user who started the game and gets the notification.
    user_2 : ``ClientUserBase``
        The user who accepted the challenge.
    timestamp : `datetime`
        When the event was created.
    emoji : ``Emoji``
        The player's emoji.
    
    Raises
    ------
    DiscordException
        - If an unexpected exception occurred.
    """
    channel = await client.channel_private_create(user_1)
    
    embed = Embed(
        None,
        f'You are {emoji}\n\n**Good luck!**',
        color = 0x8000AB,
        timestamp = timestamp,
    ).add_author(
        f'{user_2.full_name} accepted your X-O-X challenge',
        user_2.avatar_url_as(size = 64),
        url = message.url,
    )
    
    guild = event.guild
    if (guild is not None):
        source_channel = event.channel
        if source_channel is None:
            channel_name = '???'
        else:
            channel_name = source_channel.name
        
        embed.add_footer(
            f'{guild.name} • {channel_name}',
            guild.icon_url_as(size = 64)
        )
    
    try:
        await client.message_create(
            channel,
            embed = embed,
            components = create_button(
                label = 'Go to message',
                url = message.url,
            )
        )
    except ConnectionError:
        # No Internet
        return
    
    except DiscordException as err:
        if err.code != ERROR_CODES.cannot_message_user:
            raise



async def xox_multi_player(client, event):
    """
    The X-O-X game against someone.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    user_1 = event.user
    timestamp = event.created_at
    
    embed = Embed(
        timestamp = timestamp,
    ).add_author(
        f'Challenge {user_1.full_name} in X-O-X!',
        user_1.avatar_url_as(size = 64),
    ).add_footer(
        'This message times out after 300 seconds.',
    )
    
    await client.interaction_application_command_acknowledge(event)
    message = await client.interaction_followup_message_create(
        event, embed = embed, components = BUTTON_CHALLENGE_ENABLED
    )
    
    try:
        event = await wait_for_component_interaction(
            message,
            timeout = 300.0,
            check = partial_func(check_event_other_user, user_1),
        )
    except TimeoutError:
        
        embed = Embed(
            timestamp = timestamp,
        ).add_author(
            f'Challenge {user_1.full_name} X-O-X!',
            user_1.avatar_url_as(size = 64),
        ).add_footer(
            'This message timed out.',
        )
        
        await client.interaction_response_message_edit(event, embed = embed, components = BUTTON_CHALLENGE_DISABLED)
        
        return
    
    user_2 = event.user
    
    array = [0 for _ in range(9)]
    
    if random() < 0.5:
        user_1_settings = PLAYER_SETTINGS_KOISHI
        user_2_settings = PLAYER_SETTINGS_SATORI
    else:
        user_1_settings = PLAYER_SETTINGS_SATORI
        user_2_settings = PLAYER_SETTINGS_KOISHI
    
    users = (user_1, user_2)
    user_settings = (user_1_settings, user_2_settings)
    
    player_index = (random() < 0.5)
    
    Task(KOKORO, try_send_notification(client, event, message, user_1, user_2, timestamp, user_1_settings.emoji))
    
    title = f'It is your turn {users[player_index].mention} | {user_settings[player_index].emoji}'
    
    await client.interaction_component_message_edit(
        event,
        title,
        embed = None,
        components = render_components(array, False, user_1_settings, user_2_settings),
    )
    
    while True:
        try:
            event = await wait_for_component_interaction(
                event,
                timeout = 300.0,
                check = partial_func(check_event_user, users[player_index]),
            )
        except TimeoutError:
            await client.interaction_response_message_edit(
                event,
                'Timeout occurred.',
                components = render_components(array, True,  user_1_settings, user_2_settings),
            )
            break
        
        if not click(
            array, event.interaction.custom_id, user_settings[player_index].identifier
        ):
            await client.interaction_component_acknowledge(event)
            continue
        
        game_state = get_game_state(array, user_settings[player_index].identifier)
        if game_state == GAME_STATE_NONE:
            player_index ^= 1
            
            await client.interaction_component_message_edit(
                event,
                f'It is your turn {users[player_index].mention} | {user_settings[player_index].emoji.as_emoji}',
                components = render_components(array, False, user_1_settings, user_2_settings),
            )
            continue
        
        if game_state == GAME_STATE_DRAW:
            title = 'Draw'
        else:
            player_index ^= game_state != GAME_STATE_P1_WIN
            title = f'{users[player_index].full_name} won against {users[player_index ^ 1].full_name}'
        
        await client.interaction_component_message_edit(
            event,
            title,
            components = render_components(array, True, user_1_settings, user_2_settings),
        )
        break
