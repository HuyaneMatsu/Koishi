__all__ = ('command_automation_reaction_role_entry_create', 'command_automation_reaction_role_entry_list')

from hata import CHANNELS, Client, DiscordException, ERROR_CODES, MESSAGES, parse_message_reference

from .component_builders import (
    build_automation_reaction_role_listing_components, build_automation_reaction_role_entry_overview_components
)
from .constants import ENTRIES_MAX
from .helpers import get_automation_reaction_role_entry_listing_and_sync_page, get_or_create_automation_reaction_role_entry


async def command_automation_reaction_role_entry_create(
    client,
    interaction_event,
    message: (str, 'Please reference a message!'),
):
    """
    Adds roles if the users reacts on a message. (Admin only)
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    message : `str`
        The referenced message.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        if not interaction_event.user_permissions.administrator:
            error_message = 'You must have `administrator` permission to invoke this command.'
            break
        
        permissions = interaction_event.application_permissions
        if (not permissions.manage_messages) or (not permissions.manage_roles):
            error_message = 'I need to have `manage messages` and `manage roles` permissions to execute this command.'
            break
        
        guild = interaction_event.guild
        if guild is None:
            error_message = 'Guild only command.'
            break
        
        if client.get_guild_profile_for(guild) is None:
            error_message = 'I must be in the guild to execute this command.'
            break
        
        message_reference = parse_message_reference(message)
        if message_reference is None:
            error_message = 'Could not identify the message.'
            break
        
        guild_id, channel_id, message_id = message_reference
        if guild_id and (guild_id != guild.id):
            error_message = 'The message belongs to an other guild.'
            break
        
        while True:
            try:
                target_message = MESSAGES[message_id]
            except KeyError:
                pass
            else:
                if target_message.guild_id != guild.id:
                    error_message = 'The message belongs to an other guild.'
                    break
            
            if not channel_id:
                channel = interaction_event.channel
            else:
                try:
                    channel = CHANNELS[channel_id]
                except KeyError:
                    error_message = 'I have no access to the channel.'
                    break
                
                else:
                    if channel.guild_id != guild.id:
                        error_message = 'The message belongs to an other guild.'
                        break
            
            if not channel.cached_permissions_for(client).read_message_history:
                error_message = 'I need read message history permission to requested the selected message.'
                break
            
            try:
                target_message = await client.message_get((channel.id, message_id),)
            except ConnectionError:
                # No internet
                return
            
            except DiscordException as err:
                if err.code in (
                    ERROR_CODES.unknown_channel, # message deleted
                    ERROR_CODES.unknown_message, # channel deleted
                ):
                    error_message = 'The referenced message does not exist.'
                    break
                
                if err.code == ERROR_CODES.missing_access: # client removed
                    return
                
                if err.code == ERROR_CODES.missing_permissions:
                    error_message = 'I have no permission to get that message.'
                    break
                
                raise
            
            error_message = None
            break
            
        if (error_message is not None):
            break
        
        automation_reaction_role_entry, listing_page_index = await get_or_create_automation_reaction_role_entry(
            target_message
        )
        if (automation_reaction_role_entry is None):
            error_message = f'Max {ENTRIES_MAX} auto react roles are allowed.'
            break
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            allowed_mentions = None,
            components = build_automation_reaction_role_entry_overview_components(
                client,
                listing_page_index,
                automation_reaction_role_entry,
                0,
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )


async def command_automation_reaction_role_entry_list(
    client,
    interaction_event,
):
    """
    Shows the auto react roles of the guild.
    
    This function is a coroutine
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    while True:
        if not interaction_event.user_permissions.administrator:
            error_message = 'You must have `administrator` permission to invoke this command.'
            break
        
        guild = interaction_event.guild
        if guild is None:
            error_message = 'Guild only command.'
            break
        
        if client.get_guild_profile_for(guild) is None:
            error_message = 'I must be in the guild to execute this command.'
            break
        
        automation_reaction_role_entry_listing = await get_automation_reaction_role_entry_listing_and_sync_page(
            guild.id, 0
        )
        
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        
        await client.interaction_followup_message_create(
            interaction_event,
            components = build_automation_reaction_role_listing_components(
                guild,
                automation_reaction_role_entry_listing,
                0,
            ),
        )
        return
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = error_message,
    )
