__all__ = ('command_user_inspect_equipment',)

from hata import create_text_display
from hata.ext.slash import P

from ..item_core import ITEM_FLAG_COSTUME, ITEM_FLAG_HEAD, get_item_nullable
from ..user_equip import ITEM_FLAGS_ALLOWED, ITEM_SLOTS, ITEM_SLOT_NAMES
from ..user_inspect_item import produce_item_inspect_description

from ..user_stats_core import get_user_stats


async def command_user_inspect_equipment(
    client,
    interaction_event,
    item_slot : P([(name, format(value, 'x')) for name, value in ITEM_SLOTS], 'Select an item slot'),
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
        user_stats = await get_user_stats(interaction_event.user_id)
        
        if item_slot == ITEM_FLAG_HEAD:
            item_id = user_stats.item_id_head
        elif item_slot == ITEM_FLAG_COSTUME:
            item_id = user_stats.item_id_costume
        else:
            item_id = user_stats.item_id_weapon
        
        item = get_item_nullable(item_id)
        if item is None:
            error_message = f'You cannot inspect {ITEM_SLOT_NAMES[item_slot]!s}, you do not have such an item.'
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
