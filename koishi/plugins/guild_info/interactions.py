__all__ = ()

from ...bots import FEATURE_CLIENTS

from .constants import GUILD_INFO_SELECT_CUSTOM_ID
from .component_building import build_guild_info_components


@FEATURE_CLIENTS.interactions(custom_id = GUILD_INFO_SELECT_CUSTOM_ID)
async def guild_info_component_command(client, interaction_event, *, values):
    """
    Handles a guild info select interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    values : `None | tuple<str>`
        The selected value.
    """
    if interaction_event.message.interaction.user_id != interaction_event.user_id:
        return
    
    if values is None:
        return
     
    try:
        guild_info_flags = int(values[0], 16)
    except ValueError:
        return
    
    guild = interaction_event.guild
    if guild is None:
        await client.interaction_component_acknowledge(
            interaction_event,
        )
        await client.interaction_followup_message_create(
            interaction_event,
            content = 'I must be in the guild to execute this command.',
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_component_message_edit(
        interaction_event,
        components = build_guild_info_components(guild, guild_info_flags),
    )
