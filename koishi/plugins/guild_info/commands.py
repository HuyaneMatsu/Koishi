__all__ = ('command_guild_info',)

from .constants import GUILD_INFO_FLAG_INFO, GUILD_INFO_FLAGS
from .component_building import build_guild_info_components


async def command_guild_info(
    client,
    interaction_event,
    guild_info_flags: (GUILD_INFO_FLAGS, 'Which fields should I show?', 'field') = GUILD_INFO_FLAG_INFO,
):
    """
    Shows some information about the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    guild_info_flags : `int` = `GUILD_INFO_FLAG_INFO`, Optional
        The flags to show field based on.
    """
    guild = interaction_event.guild
    if guild is None:
        await client.interaction_response_message_create(
            interaction_event,
            content = 'I must be in the guild to execute this command.',
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        components = build_guild_info_components(guild, guild_info_flags),
    )
