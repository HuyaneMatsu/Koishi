__all__ = ()

from hata.ext.slash import InteractionResponse, Option, Row, Select

from .constants import (
    BUTTON_SNIPE_ACTIONS_DISABLED, BUTTON_SNIPE_ACTIONS_EMOJI, BUTTON_SNIPE_ACTIONS_STICKER, BUTTON_SNIPE_CLOSE,
    BUTTON_SNIPE_DETAILS_DISABLED, BUTTON_SNIPE_DETAILS_EMOJI, BUTTON_SNIPE_DETAILS_REACTION,
    BUTTON_SNIPE_DETAILS_STICKER, BUTTON_SNIPE_DM, BUTTON_SNIPE_REVEAL, BUTTON_SNIPE_REVEAL_DISABLED,
    CUSTOM_ID_SNIPE_SELECT_EMOJI, CUSTOM_ID_SNIPE_SELECT_REACTION, CUSTOM_ID_SNIPE_SELECT_STICKER
)
from .embed_builder_common import embed_builder_emoji, embed_builder_reaction, embed_builder_sticker


def select_option_builder_emoji(emoji):
    """
    Builds a select option for the given emoji.
    
    Parameters
    ----------
    emoji : ``Emoji``
        The emoji to create option for.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return Option(emoji.as_emoji, emoji.name, emoji)


def select_option_builder_sticker(sticker):
    """
    Builds a select option for the given sticker.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The sticker to create option for.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return Option(str(sticker.id), sticker.name)


def build_initial_response_parts_factory(
    embed_builder, select_option_builder, select_custom_id, button_details_enabled, button_actions_enabled
):
    """
    Returns an initial response builder.
    
    Parameters
    ----------
    embed_builder : `FunctionType`
        An embed builder to build the response with.
        
        The accepted implementations are:
        - `(Client, InteractionEvent, Emoji, None | str, bool) -> Coroutine<Embed>`
        - `(Client, InteractionEvent, Sticker, None | str, bool) -> Coroutine<Embed>`
        
        Actual implementations:
        - ``embed_builder_emoji``
        - ``embed_builder_reaction``
        - ``embed_builder_sticker``
    
    select_option_builder : `FunctionType`
        Select option builder. used when there are over 1 options.
        
        The accepted implementations are:
        - `(Emoji) -> StringSelectOption`
        - `(Sticker) -> StringSelectOption`
        
        Actual implementations:
        - ``select_option_builder_emoji``
        - ``select_option_builder_sticker``
    
    select_custom_id : `str`
        Custom id used for the select as required.
    
    button_details_enabled : ``Component``
        Enabled `details` button.
    
    button_actions_enabled : ``Component``
        Enabled `actions` button.
    
    Returns
    -------
    response_parts_builder : `CoroutineFunctionType`
        The returned builder is implemented as:
        - `(Client, InteractionEvent, list<Emoji>, bool, bool) -> Coroutine<Embed, list<Component>>`
        - `(Client, InteractionEvent, list<Sticker>, bool, bool) -> Coroutine<Embed, list<Component>>`
    """
    async def build_initial_response_parts_generic(
        client, event, target, entities, show_for_invoking_user_only, detailed
    ):
        """
        Builds initial response parts for a snipe command.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the event.
        event : ``InteractionEvent``
            The received interaction event.
        target : `None`, ``Message``
            The target message type.
        entities : (`list` of ``Emoji``), (`list` of ``Sticker``)
            Entities in context.
        show_for_invoking_user_only : `bool`
            Whether the message is an invoking user only message.
        
        Returns
        -------
        interaction_response : ``InteractionResponse``
        """
        nonlocal button_actions_enabled
        nonlocal button_details_enabled
        nonlocal embed_builder
        nonlocal select_option_builder
        nonlocal select_custom_id
        
        if target is None:
            target_url = None
        else:
            target_url = target.url
        
        entity = entities[0]
        
        embed = await embed_builder(client, event, entity, target_url, detailed)
        
        if show_for_invoking_user_only:
            button_reveal = BUTTON_SNIPE_REVEAL
        else:
            button_reveal = BUTTON_SNIPE_REVEAL_DISABLED
        
        if detailed:
            button_details = BUTTON_SNIPE_DETAILS_DISABLED
        else:
            button_details = button_details_enabled
        
        if event.guild_id:
            button_actions = button_actions_enabled
        else:
            button_actions = BUTTON_SNIPE_ACTIONS_DISABLED
        
        components = []
        
        if len(entities) > 1:
            del entities[25:]
            
            components.append(
                Row(
                    Select(
                        [select_option_builder(entity) for entity in entities],
                        custom_id = select_custom_id,
                        placeholder = 'Select an emoji!',
                    ),
                )
            )
        
        components.append(
            Row(
                button_details,
                BUTTON_SNIPE_DM,
                button_actions,
                button_reveal,
                BUTTON_SNIPE_CLOSE,
            )
        )
        
        return embed, components
    
    return build_initial_response_parts_generic


def build_initial_response_factory(response_parts_builder):
    """
    Returns an initial response builder.
    
    Parameters
    ----------
    response_parts_builder : `CoroutineFunctionType`
        A coroutine function to create the response parts with.
        
        The accepted implementations are:
        - `(Client, InteractionEvent, list<Emoji>, bool, bool) -> Coroutine<Embed, list<Component>>`
        - `(Client, InteractionEvent, list<Sticker>, bool, bool) -> Coroutine<Embed, list<Component>>`
        
        Actual implementations:
        - ``build_initial_response_parts_emoji``
        - ``build_initial_response_parts_reaction``
        - ``build_initial_response_parts_sticker``
    
    Returns
    -------
    response_builder : `CoroutineFunctionType`
        The returned builder is implemented as:
        - `(Client, InteractionEvent, {None, Message}, list<Emoji>, bool, bool) -> Coroutine<InteractionResponse>`
        - `(Client, InteractionEvent, {None, Message}, list<Sticker>, bool, bool) -> Coroutine<InteractionResponse>`
    """
    async def build_initial_response_generic(client, event, target, entities, show_for_invoking_user_only, detailed):
        """
        Builds initial response for a snipe command.
        
        This function is a coroutine.
        
        Parameters
        ----------
        client : ``Client``
            The client who received the interaction event.
        event : ``InteractionEvent``
            The received interaction event.
        target : `None`, ``Message``
            The target message type.
        entities : (`list` of ``Emoji``), (`list` of ``Sticker``)
            Entities in context.
        show_for_invoking_user_only : `bool`
            Whether the message is an invoking user only message.
        detailed : `bool`
            Whether detailed response should be shown.
        
        Returns
        -------
        interaction_response : ``InteractionResponse``
        """
        nonlocal response_parts_builder
        
        embed, components = await response_parts_builder(
            client, event, target, entities, show_for_invoking_user_only, detailed
        )
        return InteractionResponse(
            embed = embed, components = components, show_for_invoking_user_only = show_for_invoking_user_only
        )

    return build_initial_response_generic


build_initial_response_parts_emoji = build_initial_response_parts_factory(
    embed_builder_emoji,
    select_option_builder_emoji,
    CUSTOM_ID_SNIPE_SELECT_EMOJI,
    BUTTON_SNIPE_DETAILS_EMOJI,
    BUTTON_SNIPE_ACTIONS_EMOJI,
)

build_initial_response_parts_reaction = build_initial_response_parts_factory(
    embed_builder_reaction,
    select_option_builder_emoji,
    CUSTOM_ID_SNIPE_SELECT_REACTION,
    BUTTON_SNIPE_DETAILS_REACTION,
    BUTTON_SNIPE_ACTIONS_EMOJI,
)

build_initial_response_parts_sticker = build_initial_response_parts_factory(
    embed_builder_sticker,
    select_option_builder_sticker,
    CUSTOM_ID_SNIPE_SELECT_STICKER,
    BUTTON_SNIPE_DETAILS_STICKER,
    BUTTON_SNIPE_ACTIONS_STICKER,
)

build_initial_response_emoji = build_initial_response_factory(build_initial_response_parts_emoji)
build_initial_response_reaction = build_initial_response_factory(build_initial_response_parts_reaction)
build_initial_response_sticker = build_initial_response_factory(build_initial_response_parts_sticker)
