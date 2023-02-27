__all__ = ()

from hata import Client

from .cache_sticker import get_sticker
from .component_translate_tables import DETAILS_DISABLE
from .constants import CUSTOM_ID_SNIPE_DETAILS_EMOJI, CUSTOM_ID_SNIPE_DETAILS_STICKER
from .embed_builder_common import embed_builder_emoji, embed_builder_reaction, embed_builder_sticker
from .embed_parsers import get_emoji_from_event, get_entity_id_from_event, parse_source_message_url
from .helpers import translate_components


SLASH_CLIENT: Client


async def parse_back_emoji(client, event):
    """
    Parses the emoji back from the given event's message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    return get_emoji_from_event(event)


async def parse_back_sticker(client, event):
    """
    Parses the sticker back from the given event's message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    sticker : `None`, ``Sticker``
    """
    sticker_id = get_entity_id_from_event(event)
    if sticker_id:
        return await get_sticker(client, sticker_id)



async def snipe_interaction_respond_common(client, event, entity_back_parser, embed_builder):
    """
    Shared function used by entity detail shower component commands.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    entity_back_parser : `CoroutineFunctionType`
        Parser to get the entity in context back.
        
        The accepted implementations are:
        - `(Client, InteractionEvent) -> Coroutine<None | Emoji>`
        - `(Client, InteractionEvent) -> Coroutine<None | Sticker>`
        
        Actual implementations:
        - ``parse_back_emoji``
        - ``parse_back_sticker``
    
    embed_builder : `CoroutineFunctionType`
        Embed builder to build the response embed with.
        
        The accepted implementations are:
        - `(Client, InteractionEvent, Emoji, None | str, bool) -> Coroutine<Embed>`.
        - `(Client, InteractionEvent, Sticker, None | str, bool) -> Coroutine<Embed>`.
        
        Actual implementations:
        - ``embed_builder_emoji``
        - ``embed_builder_reaction``
        - ``embed_builder_sticker``
    """
    await client.interaction_component_acknowledge(event, wait = False)
    
    entity = await entity_back_parser(client, event)
    
    embed = await embed_builder(client, event, entity, parse_source_message_url(event.message), True)
    
    await client.interaction_response_message_edit(
        event,
        embed = embed,
        components = translate_components(event.message.iter_components(), DETAILS_DISABLE),
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DETAILS_EMOJI)
async def snipe_interaction_emoji_details(client, event):
    """
    Changes the embed to show the emoji's details. Also disabled the `details` button.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await snipe_interaction_respond_common(client, event, parse_back_emoji, embed_builder_emoji)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DETAILS_STICKER)
async def snipe_interaction_sticker_details(client, event):
    """
    Changes the embed to show the reaction's details. Also disabled the `details` button.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await snipe_interaction_respond_common(client, event, parse_back_emoji, embed_builder_reaction)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DETAILS_STICKER)
async def snipe_interaction_sticker_details(client, event):
    """
    Changes the embed to show the sticker's details. Also disabled the `details` button.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await snipe_interaction_respond_common(client, event, parse_back_sticker, embed_builder_sticker)
