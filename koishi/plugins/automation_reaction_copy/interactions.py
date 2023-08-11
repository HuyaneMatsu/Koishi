__all__ = ()

from ...bots import SLASH_CLIENT

from ..automation_core import get_reaction_copy_enabled_and_role

from .constants import CUSTOM_ID_CLOSE, CUSTOM_ID_REFRESH
from .list_channels import build_reaction_copy_list_channels_response


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_REFRESH)
async def page_refresh(client, event):
    """
    Refreshes the reaction-copy message.
    
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
    guild = event.guild
    if (guild is None):
        return
    
    enabled, role = get_reaction_copy_enabled_and_role(guild.id)
    if event.user_permissions.can_administrator or ((role is not None) and event.user.has_role(role)):
        return build_reaction_copy_list_channels_response(client, guild, enabled)


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_CLOSE)
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
    if event.user_permissions.can_manage_messages:
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)
