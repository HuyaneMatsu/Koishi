__all__ = ()

from hata import Client
from hata.ext.slash import InteractionResponse, abort

from ...bots import FEATURE_CLIENTS

from .constants import CUSTOM_ID_CONTINUOUS_RP, CUSTOM_ID_INITIAL_RP
from .helpers import flip_tile, generate_flipped_tiles, generate_tiles, get_tile_map
from .parsers import parse_back_tiles
from .renderers import render_continuous, render_initial



async def check_invoking_user(client, event):
    """
    Checks whether the invoking user is the same as the original invoking user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    passed : `bool`
    """
    if event.message.interaction.user_id == event.user_id:
        return True
    
    await client.interaction_component_acknowledge(event)
    await client.interaction_followup_message_create(
        event,
        'You must be the original invoker of the command',
        show_for_invoking_user_only = True,
    )
    return False


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)
async def minesweeper(
    client,
    event,
    bomb_count: (range(4, 16), 'how much bombs should there be') = 4,
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
    bomb_count : `int` = `4`, Optional
        The amount of bombs to initialise the game with.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.channel.slowmode and (not event.channel.cached_permissions_for(client).manage_messages):
        return abort('Please use the command in a channel without slowmode.')
    
    return InteractionResponse(components = render_initial(bomb_count))


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_INITIAL_RP)
async def flip_initial(client, event, index, bomb_count):
    """
    Executes an initial flip on the game.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    index : `str`
        The index of the flipped tile. later converted to `int`.
    bomb_count : `str`
        The total amount of bombs to render. Later converted to `int`.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    if not await check_invoking_user(client, event):
        return
    
    index = int(index)
    bomb_count = int(bomb_count)
    
    tiles = generate_tiles(index, bomb_count)
    flipped_tiles = generate_flipped_tiles()
    flip_tile(tiles, flipped_tiles, index)
    tile_map = get_tile_map(client.id)
    return InteractionResponse(components = render_continuous(tiles, flipped_tiles, tile_map))


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CONTINUOUS_RP)
async def flip_continuous(client, event, index):
    """
    Executes an flip on the game.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    index : `str`
        The index of the flipped tile. later converted to `int`.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    if not await check_invoking_user(client, event):
        return
    
    index = int(index)
    
    back_parse = parse_back_tiles(event)
    if back_parse is None:
        await client.interaction_component_acknowledge(event)
        await client.interaction_followup_message_create(
            event,
            'Failed to re-construct game state',
            show_for_invoking_user_only = True,
        )
        return
    
    flip_tile(*back_parse, index)
    tile_map = get_tile_map(client.id)
    return InteractionResponse(components = render_continuous(*back_parse, tile_map))
