__all__ = ()

from hata import Client
from hata.ext.slash import Row

from .cache_sticker import get_sticker
from .constants import (
    BUTTON_SNIPE_ACTIONS_DISABLED, BUTTON_SNIPE_ADD_DISABLED, BUTTON_SNIPE_ADD_EMOJI, BUTTON_SNIPE_ADD_STICKER,
    BUTTON_SNIPE_EDIT_DISABLED, BUTTON_SNIPE_EDIT_EMOJI, BUTTON_SNIPE_EDIT_STICKER, BUTTON_SNIPE_REMOVE_DISABLED,
    BUTTON_SNIPE_REMOVE_EMOJI, BUTTON_SNIPE_REMOVE_STICKER, CUSTOM_ID_SNIPE_ACTIONS_EMOJI,
    CUSTOM_ID_SNIPE_ACTIONS_STICKER
)
from .embed_parsers import get_emoji_from_event, get_entity_id_from_event
from .helpers import check_has_manage_emojis_and_stickers_permission, translate_components


SLASH_CLIENT: Client

DISABLED_TABLE_ACTIONS = {
    CUSTOM_ID_SNIPE_ACTIONS_EMOJI: BUTTON_SNIPE_ACTIONS_DISABLED,
    CUSTOM_ID_SNIPE_ACTIONS_STICKER: BUTTON_SNIPE_ACTIONS_DISABLED,
}


def iter_action_components_factory(button_add, button_edit, button_remove):
    """
    Returns an action component iterator.
    
    Parameters
    ----------
    button_add : ``Component``
        Component triggering adding the entity.
    button_edit : ``Component``
        Component triggering editing the entity.
    button_remove : ``Component``
        Component triggering removing the entity.
    
    Returns
    ------
    iter_action_components : `GeneratorType`
        The produced generator has the following implementation:
        - `(InteractionEvent, Emoji | Sticker) -> Generator<Component>`
    """
    def iter_action_components_generic(event, entity):
        """
        Iterates over the action components applicable for the given `event` - `entity` combination.
        
        This function is an iterable generator.
        
        Parameters
        ----------
        event : ``InteractionEvent``
            The received interaction event.
        entity : ``Sticker``, ``Emoji``
            The entity in context.
        
        Yields
        ------
        component : ``Component``
        """
        nonlocal button_add
        nonlocal button_edit
        nonlocal button_remove
        
        event_guild_id = event.guild_id
        entity_guild_id = entity.guild_id
        
        if (event_guild_id == 0):
            yield BUTTON_SNIPE_ADD_DISABLED
            yield BUTTON_SNIPE_EDIT_DISABLED
            yield BUTTON_SNIPE_REMOVE_DISABLED
        
        elif (event_guild_id == entity_guild_id):
            yield BUTTON_SNIPE_ADD_DISABLED
            yield button_edit
            yield button_remove
        
        else:
            yield button_add
            yield BUTTON_SNIPE_EDIT_DISABLED
            yield BUTTON_SNIPE_REMOVE_DISABLED
    
    return iter_action_components_generic


iter_action_components_emoji = iter_action_components_factory(
    BUTTON_SNIPE_ADD_EMOJI, BUTTON_SNIPE_EDIT_EMOJI, BUTTON_SNIPE_REMOVE_EMOJI
)
iter_action_components_sticker = iter_action_components_factory(
    BUTTON_SNIPE_ADD_STICKER, BUTTON_SNIPE_EDIT_STICKER, BUTTON_SNIPE_REMOVE_STICKER
)


async def parse_and_get_emoji(client, event):
    """
    Parses the emoji from the event's message and returns it.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    emoji : `None`, ``Emoji``
    """
    return get_emoji_from_event(event)


async def parse_and_get_sticker(client, event):
    """
    Parses the sticker from the event's message and returns it.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    sticker : `None`, ``Sticker``
    """
    sticker_id = get_entity_id_from_event(event)
    if sticker_id:
        return await get_sticker(client, sticker_id)


async def respond_with_actions(client, event, entity_parser, action_component_iterator):
    """
    Edits the message's components adding the given row.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    entity_parser : `CoroutineFunctionType`
        Parses the entity out from the event's message.
        
        The accepted implementations are:
        - `(Client, InteractionEvent) -> Coroutine<None | Emoji>`
        - `(Client, InteractionEvent) -> Coroutine<None | Sticker>`
        
        Actual implementations:
        - ``parse_and_get_emoji``
        - ``parse_and_get_sticker``
    
    action_component_iterator : `GeneratorFunctionType`
        Yields the action row's components.
        
        The accepted implementations are:
        - `(InteractionEvent, Emoji | Sticker) -> Generator<Component>`
        
        Actual implementations:
        - ``iter_action_components_emoji``
        - ``iter_action_components_sticker``
    """
    if not await check_has_manage_emojis_and_stickers_permission(client, event):
        return
    
    await client.interaction_component_acknowledge(event, wait = False)
    
    entity = await entity_parser(client, event)
    if event is None:
        return
    
    components = translate_components(event.message.iter_components(), DISABLED_TABLE_ACTIONS)
    components.append(Row(*action_component_iterator(event, entity)))
    
    await client.interaction_response_message_edit(
        event,
        components = components,
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_ACTIONS_EMOJI)
async def snipe_interaction_actions_emoji(client, event):
    """
    Adds the possible actions to the message as additional operations.
    
    > Emoji version.
    
    This function is a generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await respond_with_actions(client, event, parse_and_get_emoji, iter_action_components_emoji)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_ACTIONS_STICKER)
async def snipe_interaction_actions_sticker(client, event):
    """
    Adds the possible actions to the message as additional operations.
    
    > Sticker version.
    
    This function is a generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    """
    await respond_with_actions(client, event, parse_and_get_sticker, iter_action_components_sticker)
