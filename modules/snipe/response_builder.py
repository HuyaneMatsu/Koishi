__all__ = ()

from hata.ext.slash import InteractionResponse, Row, Select

from .constants import (
    BUTTON_SNIPE_ACTIONS_DISABLED, BUTTON_SNIPE_CLOSE, BUTTON_SNIPE_DETAILS_DISABLED, BUTTON_SNIPE_DM,
    BUTTON_SNIPE_REVEAL, BUTTON_SNIPE_REVEAL_DISABLED, CUSTOM_ID_SNIPE_SELECT
)


async def build_initial_response_parts(client, event, target, choices, show_for_invoking_user_only, detailed):
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
    choices : `list` of ``ChoiceBase``
        Entities in context.
    show_for_invoking_user_only : `bool`
        Whether the message is an invoking user only message.
    
    Returns
    -------
    interaction_response : ``InteractionResponse``
    """
    if target is None:
        target_url = None
    else:
        target_url = target.url
    
    entity, choice_type = choices[0]
    
    embed = await choice_type.build_embed(entity, client, event, target_url, detailed)
    
    if show_for_invoking_user_only:
        button_reveal = BUTTON_SNIPE_REVEAL
    else:
        button_reveal = BUTTON_SNIPE_REVEAL_DISABLED
    
    if detailed:
        button_details = BUTTON_SNIPE_DETAILS_DISABLED
    else:
        button_details = choice_type.button_details_enabled
    
    if event.guild_id:
        button_actions = choice_type.button_actions_enabled
    else:
        button_actions = BUTTON_SNIPE_ACTIONS_DISABLED
    
    components = []
    
    if len(choices) > 1:
        del choices[25:]
        
        components.append(
            Row(
                Select(
                    [choice.type.select_option_builder(choice.entity) for choice in choices],
                    custom_id = CUSTOM_ID_SNIPE_SELECT,
                    placeholder = 'Select an entity!',
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


async def build_initial_response(client, event, target, choices, show_for_invoking_user_only, detailed):
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
    choices : `list` of ``ChoiceBase``
        The choices in context.
    show_for_invoking_user_only : `bool`
        Whether the message is an invoking user only message.
    detailed : `bool`
        Whether detailed response should be shown.
    
    Returns
    -------
    interaction_response : ``InteractionResponse``
    """
    embed, components = await build_initial_response_parts(
        client, event, target, choices, show_for_invoking_user_only, detailed
    )
    return InteractionResponse(
        embed = embed, components = components, show_for_invoking_user_only = show_for_invoking_user_only
    )
