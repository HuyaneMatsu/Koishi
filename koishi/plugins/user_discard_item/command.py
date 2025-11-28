__all__ = ('user_discard_item_command',)

from math import floor, inf, isnan as is_nan

from hata.ext.slash import P

from .actions import discard_item, get_discard_item_suggestions
from .content_building import produce_successful_item_discard_description


async def autocomplete_item(interaction_event, value):
    """
    Autocompletes the item to discard.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The typed in value.
    
    Returns
    -------
    suggestions : `None | list<(str, int)>`
    """
    return await get_discard_item_suggestions(interaction_event.user_id, value)


async def user_discard_item_command(
    client,
    interaction_event,
    item_name : P(str, 'The item\'s name', 'item', autocomplete = autocomplete_item),
    amount : ('expression', 'The amount of items to discard.'),
):
    """
    Discard items from your inventory.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_slot : `int`
        The selected user.
    
    item_name : `str`
        The give item name.
    
    amount : `int | float`
    
    Returns
    -------
    response : ``Embed``
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        if isinstance(amount, float):
            if is_nan(amount):
                amount = 0
            
            elif amount == inf:
                amount = (1 << 64) - 1
            
            elif amount == -inf:
                amount = -1
            
            else:
                amount = floor(amount)
        
        if amount <= 0:
            error_message = 'You cannot discard less than 1 items.'
            break
        
        item, discarded_amount, new_amount = await discard_item(interaction_event.user_id, item_name, amount)
        if item is None:
            error_message = f'Could not discard {item_name!s}, you do not have such an item.'
            break
        
        if not discarded_amount:
            error_message = f'You did not discard any of your {new_amount} {item.name}.'
            break
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            content = ''.join([*produce_successful_item_discard_description(item, discarded_amount, new_amount)])
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )
