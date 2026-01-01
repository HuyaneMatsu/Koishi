__all__ = ('command_user_inspect_item',)

from hata import create_text_display
from hata.ext.slash import P

from ..inventory_core import create_item_suggestions, get_inventory, select_item

from .content_building import produce_item_inspect_description


async def autocomplete_item(interaction_event, value):
    """
    Autocompletes the item to inspect.
    
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
    inventory = await get_inventory(interaction_event.user_id)
    return create_item_suggestions(inventory, 0, value)


async def command_user_inspect_item(
    client,
    interaction_event,
    item_name : P(str, 'The item\'s name.', 'item', autocomplete = autocomplete_item),
):
    """
    Inspects the select item from your inventory.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_name : `str`
        The selected item's name.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        inventory = await get_inventory(interaction_event.user_id)
        item = select_item(inventory, 0, item_name)
        if item is None:
            error_message = f'You cannot inspect {item_name!s}, you do not have such an item.'
            break
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = [
                create_text_display(''.join([*produce_item_inspect_description(item)]))
            ],
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )
    return
