__all__ = ('command_user_equip', 'command_user_unequip')

from hata.ext.slash import P

from ..inventory_core import create_item_suggestions, get_inventory

from .actions import equip_item, unequip_item
from .constants import ITEM_FLAGS_ALLOWED, ITEM_SLOTS, ITEM_SLOT_NAMES, ITEM_SLOT_NAME_UNKNOWN


async def autocomplete_item(interaction_event, value):
    """
    Autocompletes the item to equip. Item type must be selected already.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The typed in value.
    
    Returns
    -------
    suggestions : `None | list<(str, str)>`
    """
    item_slot = interaction_event.get_value_of('equip', 'item-slot')
    if item_slot is None:
        return
    
    try:
        item_slot = int(item_slot, 16)
    except ValueError:
        return
    
    if item_slot not in ITEM_FLAGS_ALLOWED:
        return
    
    inventory = await get_inventory(interaction_event.user_id)
    return create_item_suggestions(inventory, item_slot, value)


async def command_user_equip(
    client,
    interaction_event,
    item_slot : P([(name, format(value, 'x')) for name, value in ITEM_SLOTS], 'Select an item slot'),
    item_name : P(str, 'The item\'s name.', 'item', autocomplete = autocomplete_item),
):
    """
    Equips the selected item at the selected item slot.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_slot : P([(name, format(value, 'x')) for name, value in ITEM_SLOTS], 'Select an item slot'),
        The selected item slot as a strong representing a hexadecimal integer.
    
    item_name : `str`
        The given item name.
    """
    try:
        item_slot = int(item_slot, 16)
    except ValueError:
        return
    
    if item_slot not in ITEM_FLAGS_ALLOWED:
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        old_item, new_item = await equip_item(interaction_event.user_id, item_slot, item_name)
        if new_item is None:
            error_message = (
                f'Cannot equip {item_name!s} as {ITEM_SLOT_NAMES.get(item_slot, ITEM_SLOT_NAME_UNKNOWN)!s}.'
            )
            break
    
        if old_item is new_item:
            error_message = (
                f'Are you sure you do not have {new_item.name} already equipped as '
                f'{ITEM_SLOT_NAMES.get(item_slot, ITEM_SLOT_NAME_UNKNOWN)!s}?'
            )
            break
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        
        if old_item is None:
            content = (
                f'You equipped {new_item.name} as your {ITEM_SLOT_NAMES.get(item_slot, ITEM_SLOT_NAME_UNKNOWN)!s}.'
            )
        else:
            content = (
                f'You equipped {new_item.name} as your {ITEM_SLOT_NAMES.get(item_slot, ITEM_SLOT_NAME_UNKNOWN)!s}, '
                f'unequipping {old_item.name}.'
            )
        
        await client.interaction_followup_message_create(
            interaction_event,
            content = content
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )
    return


async def command_user_unequip(
    client,
    interaction_event,
    item_slot : P([(name, format(value, 'x')) for name, value in ITEM_SLOTS], 'Select an item slot'),
):
    """
    Unequips the item from the selected item slot.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    item_slot : `str`
        The selected item slot as a string representing a hexadecimal integer.
    """
    try:
        item_slot = int(item_slot, 16)
    except ValueError:
        return
    
    if item_slot not in ITEM_FLAGS_ALLOWED:
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        old_item = await unequip_item(interaction_event.user_id, item_slot)
        if old_item is None:
            error_message = (
                f'You do not have any item equipped as {ITEM_SLOT_NAMES.get(item_slot, ITEM_SLOT_NAME_UNKNOWN)!s}.'
            )
            break
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            content = (
                f'You unequipped your {ITEM_SLOT_NAMES.get(item_slot, ITEM_SLOT_NAME_UNKNOWN)!s}, {old_item.name}.'
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )
    return
