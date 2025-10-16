__all__ = ()

from hata import Client, DiscordException, ERROR_CODES
from hata.ext.slash import InteractionResponse, abort

from ...bots import FEATURE_CLIENTS

from .constants import CUSTOM_ID_CONTINUOUS_RP, CUSTOM_ID_INITIAL_RP
from .helpers import flip_tile, generate_flipped_tiles, generate_tiles, get_tile_map
from .parsers import parse_back_tiles
from .renderers import render_continuous, render_initial


async def _message_edit(client, interaction_event, components):
    """
    Tries to edit the given message.
    
    Parameters
    ----------
    client : ``InteractionEvent``
        Client to edit the message with.
    
    interaction_event : ``InteractionEvent``
        Interaction event to edit the message with.
    
    components : ``list<Component>``
        Components to edit the message with.
    """
    # Try with interaction
    try:
        await client.interaction_component_message_edit(
            interaction_event,
            components = components,
        )
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status >= 500:
            return
        
        error_code = exception.code
        if error_code == ERROR_CODES.unknown_message:
            return
        
        if error_code != ERROR_CODES.unknown_interaction:
            raise
    
    else:
        return
    
    # Try without interaction
    if not interaction_event.channel.cached_permissions_for(client).view_channel:
        return
    
    try:
        await client.message_edit(
            interaction_event.message,
            components = components,
        )
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if (
            (exception.status < 500) and
            (
                exception.code not in (
                    ERROR_CODES.unknown_message, # message deleted
                    ERROR_CODES.unknown_channel, # message's channel deleted
                    ERROR_CODES.missing_access, # client removed
                    ERROR_CODES.missing_permissions, # permissions changed meanwhile
                )
            )
        ):
            raise


async def check_invoking_user(client, interaction_event):
    """
    Checks whether the invoking user is the same as the original invoking user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    passed : `bool`
    """
    if interaction_event.message.interaction.user_id == interaction_event.user_id:
        return True
    
    await client.interaction_component_acknowledge(interaction_event)
    await client.interaction_followup_message_create(
        interaction_event,
        'You must be the original invoker of the command',
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def minesweeper(
    client,
    event,
    bomb_count: (range(4, 16), 'how much bombs should there be') = 8,
):
    """
    Initialises a minesweeper game.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    event : ``InteractionEvent``
        The source interaction event.
    
    bomb_count : `int` = `8`, Optional
        The amount of bombs to initialise the game with.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.channel.slowmode and (not event.channel.cached_permissions_for(client).manage_messages):
        return abort('Please use the command in a channel without slowmode.')
    
    return InteractionResponse(components = render_initial(bomb_count))


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_INITIAL_RP)
async def flip_initial(client, interaction_event, index, bomb_count):
    """
    Executes an initial flip on the game.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    index : `str`
        The index of the flipped tile. later converted to `int`.
    
    bomb_count : `str`
        The total amount of bombs to render. Later converted to `int`.
    """
    if not await check_invoking_user(client, interaction_event):
        return
    
    index = int(index)
    bomb_count = int(bomb_count)
    
    tiles = generate_tiles(index, bomb_count)
    flipped_tiles = generate_flipped_tiles()
    flip_tile(tiles, flipped_tiles, index)
    tile_map = get_tile_map(client.id)
    
    await _message_edit(client, interaction_event, render_continuous(tiles, flipped_tiles, tile_map))


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CONTINUOUS_RP)
async def flip_continuous(client, interaction_event, index):
    """
    Executes an flip on the game.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    index : `str`
        The index of the flipped tile. later converted to `int`.
    """
    if not await check_invoking_user(client, interaction_event):
        return
    
    index = int(index)
    
    back_parse = parse_back_tiles(interaction_event)
    if back_parse is None:
        await client.interaction_component_acknowledge(interaction_event)
        await client.interaction_followup_message_create(
            interaction_event,
            'Failed to re-construct game state',
            show_for_invoking_user_only = True,
        )
        return
    
    flip_tile(*back_parse, index)
    tile_map = get_tile_map(client.id)
    
    await _message_edit(client, interaction_event, render_continuous(*back_parse, tile_map))
