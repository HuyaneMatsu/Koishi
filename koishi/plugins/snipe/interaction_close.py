__all__ = ()

from hata import Client, DiscordException, ERROR_CODES

from ...bots import SLASH_CLIENT

from .constants import CUSTOM_ID_SNIPE_CLOSE


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_CLOSE)
async def snipe_interaction_close(client, event):
    """
    Closes the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event, wait = False)
    
    message = event.message
    if message is None:
        return
    
    if event.guild_id == 0:
        can_delete = True
    
    elif event.user_permissions.can_manage_messages:
        can_delete = True
    
    else:
        interaction = message.interaction
        if interaction is None:
            can_delete = True
        
        elif interaction.user is event.user:
            can_delete = True
        
        else:
            can_delete = False
    
    
    if not can_delete:
        await client.interaction_followup_message_create(
            event,
            'You must be the invoker of the interaction, or have manage messages permission to do this.',
            show_for_invoking_user_only = True,
        )
        return
    
    try:
        await client.interaction_response_message_delete(event)
    except ConnectionError:
        pass
    
    except DiscordException as err:
        if err.code not in (
            ERROR_CODES.unknown_message, # message deleted
            ERROR_CODES.unknown_channel, # message's channel deleted
            ERROR_CODES.missing_access, # client removed
        ):
            raise
