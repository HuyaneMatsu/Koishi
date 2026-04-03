__all__ = ()

from ...bots import FEATURE_CLIENTS

from ..automation_core import get_reaction_copy_fields_forced

from .constants import CUSTOM_ID_CLOSE, CUSTOM_ID_REFRESH
from .list_channels import build_reaction_copy_list_channels_response


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_REFRESH)
async def page_refresh(event):
    """
    Refreshes the reaction-copy message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    guild = event.guild
    if (guild is None):
        return
    
    enabled, role, flags = get_reaction_copy_fields_forced(guild.id)
    if event.user_permissions.administrator or ((role is not None) and event.user.has_role(role)):
        return build_reaction_copy_list_channels_response(guild, enabled, flags)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLOSE)
async def close_message(client, event):
    """
    Closes the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    """
    if event.user_permissions.manage_messages:
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)
