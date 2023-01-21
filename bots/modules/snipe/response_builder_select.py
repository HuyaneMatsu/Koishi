__all__ = ()

from hata import parse_emoji
from hata.ext.slash import InteractionResponse

from .cache_sticker import get_sticker
from .constants import (
    BUTTON_SNIPE_ADD_DISABLED, BUTTON_SNIPE_ADD_EMOJI, BUTTON_SNIPE_ADD_STICKER, BUTTON_SNIPE_EDIT_DISABLED,
    BUTTON_SNIPE_EDIT_EMOJI, BUTTON_SNIPE_EDIT_STICKER, BUTTON_SNIPE_REMOVE_EMOJI, BUTTON_SNIPE_REMOVE_STICKER,
    CUSTOM_ID_SNIPE_ADD_DISABLED, CUSTOM_ID_SNIPE_ADD_EMOJI, CUSTOM_ID_SNIPE_ADD_STICKER, CUSTOM_ID_SNIPE_EDIT_DISABLED,
    CUSTOM_ID_SNIPE_EDIT_EMOJI, CUSTOM_ID_SNIPE_EDIT_STICKER, CUSTOM_ID_SNIPE_REMOVE_DISABLED,
    BUTTON_SNIPE_REMOVE_DISABLED, CUSTOM_ID_SNIPE_REMOVE_EMOJI, CUSTOM_ID_SNIPE_REMOVE_STICKER
)
from .embed_builder_common import embed_builder_emoji, embed_builder_reaction, embed_builder_sticker
from .embed_parsers import parse_source_message_url
from .helpers import are_actions_allowed_for_entity, is_event_user_same, translate_components


EMOJI_OUTSIDE_TABLE = {
    CUSTOM_ID_SNIPE_ADD_DISABLED: BUTTON_SNIPE_ADD_EMOJI,
    CUSTOM_ID_SNIPE_EDIT_EMOJI: BUTTON_SNIPE_EDIT_DISABLED,
    CUSTOM_ID_SNIPE_REMOVE_EMOJI: BUTTON_SNIPE_REMOVE_DISABLED,   
}

EMOJI_INSIDE_TABLE = {
    CUSTOM_ID_SNIPE_ADD_EMOJI: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_EDIT_DISABLED: BUTTON_SNIPE_EDIT_EMOJI,
    CUSTOM_ID_SNIPE_REMOVE_DISABLED: BUTTON_SNIPE_REMOVE_EMOJI,
}

STICKER_OUTSIDE_TABLE = {
    CUSTOM_ID_SNIPE_ADD_DISABLED: BUTTON_SNIPE_ADD_STICKER,
    CUSTOM_ID_SNIPE_EDIT_STICKER: BUTTON_SNIPE_EDIT_DISABLED,
    CUSTOM_ID_SNIPE_REMOVE_STICKER: BUTTON_SNIPE_REMOVE_DISABLED,
}

STICKER_INSIDE_TABLE = {
    CUSTOM_ID_SNIPE_ADD_STICKER: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_EDIT_DISABLED: BUTTON_SNIPE_EDIT_STICKER,
    CUSTOM_ID_SNIPE_REMOVE_DISABLED: BUTTON_SNIPE_REMOVE_STICKER,
}

ALL_DISABLE_TABLE = {
    CUSTOM_ID_SNIPE_ADD_EMOJI: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_EDIT_EMOJI: BUTTON_SNIPE_EDIT_DISABLED,
    CUSTOM_ID_SNIPE_REMOVE_EMOJI: BUTTON_SNIPE_REMOVE_DISABLED,   
    CUSTOM_ID_SNIPE_ADD_STICKER: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_EDIT_STICKER: BUTTON_SNIPE_EDIT_DISABLED,
    CUSTOM_ID_SNIPE_REMOVE_STICKER: BUTTON_SNIPE_REMOVE_DISABLED,
}


def is_message_detailed(message):
    """
    Returns whether the message is showing detailed entity information.
    
    Parameters
    ----------
    message : ``Message``
        The message to check.
    
    Returns
    -------
    is_message_detailed : `bool`
    """
    embed = message.embed
    if (embed is None):
        return False
    
    fields = embed.fields
    if (fields is None):
        return False
    
    return (len(fields) > 2)


async def select_option_parser_emoji(client, event):
    """
    Parses the emoji out from the given event's select option.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``Event``
        The received event.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    selected_emojis = event.values
    if (selected_emojis is None):
        return None
    
    selected_emoji = selected_emojis[0]
    return parse_emoji(selected_emoji)


async def select_option_parser_sticker(client, event):
    """
    Parses the sticker out from the given event's select option.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``Event``
        The received event.
    
    Returns
    -------
    sticker : `None`, ``Sticker``
    """
    selected_stickers = event.values
    if (selected_stickers is None):
        return None
    
    selected_sticker = selected_stickers[0]
    try:
        selected_sticker_id = int(selected_sticker)
    except ValueError:
        return None
    
    return await get_sticker(client, selected_sticker_id)


def select_response_response_builder_factory(select_option_parser, embed_builder, table_inside, table_outside):
    """
    Creates a select response builder.
    
    Parameters
    ----------
    select_option_parser : `CoroutineFunctionType`
        Parses the selected option out from the given event.
        
        The accepted implementations are:
        - `(Client, InteractionEvent) -> Coroutine<Emoji>`
        - `(Client, InteractionEvent) -> Coroutine<Sticker>`
        
        Actual implementations:
        - ``select_option_parser_emoji``
        - ``select_option_parser_sticker``
    
    embed_builder : `CoroutineFunctionType`
        An embed builder to build the response with.
        
        The accepted implementations are:
        - `(Client, InteractionEvent, Emoji, None | str, bool) -> Coroutine<Embed>`
        - `(Client, InteractionEvent, Sticker, None | str, bool) -> Coroutine<Embed>`
        
        Actual implementations:
        - ``embed_builder_emoji``
        - ``embed_builder_reaction``
        - ``embed_builder_sticker``
    
    Returns
    -------
    response_builder : `CoroutineFunctionType`
        The returned response builder is implemented as:
        - `(Client, InteractionEvent) -> Coroutine<None | InteractionResponse>`.
    
    table_inside : `dict` of (`str`, ``Component``) items
        Component translate table to use if new entity is from inside.
    
    table_outside : `dict` of (`str`, ``Component``) items
        Component translate table to use if new entity is from outside.
    
    """
    async def select_response_response_builder_generic(client, event):
        """
        Creates a select response.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the event.
        event : ``InteractionEvent``
            The received event.
        
        Returns
        -------
        response : `None`, ``InteractionResponse``
        """
        nonlocal select_option_parser
        nonlocal embed_builder
        nonlocal table_inside
        nonlocal table_outside
        
        message = event.message
        if message is None:
            return
        
        if not is_event_user_same(event, message):
            return
        
        detailed = is_message_detailed(message)
        
        entity = await select_option_parser(client, event)
        if entity is None:
            return
        
        embed = await embed_builder(client, event, entity, parse_source_message_url(message), detailed)
        
        guild_id = event.guild_id
        if (guild_id == 0) or (not are_actions_allowed_for_entity(entity)):
            translate_table = ALL_DISABLE_TABLE
        elif (guild_id == entity.guild_id):
            translate_table = table_inside
        else:
            translate_table = table_outside
        
        return InteractionResponse(
            embed = embed,
            components = translate_components(message.iter_components(), translate_table),
        )
    
    return select_response_response_builder_generic


select_response_response_builder_emoji = select_response_response_builder_factory(
    select_option_parser_emoji, embed_builder_emoji, EMOJI_INSIDE_TABLE, EMOJI_OUTSIDE_TABLE
)

select_response_response_builder_reaction = select_response_response_builder_factory(
    select_option_parser_emoji, embed_builder_reaction, EMOJI_INSIDE_TABLE, EMOJI_OUTSIDE_TABLE
)

select_response_response_builder_sticker = select_response_response_builder_factory(
    select_option_parser_sticker, embed_builder_sticker, STICKER_INSIDE_TABLE, STICKER_OUTSIDE_TABLE
)
