__all__ = ('command_guild_quest_board', 'command_user_quests')


from ..guild_stats import get_guild_stats
from ..quest_core import get_linked_quest_listing
from ..user_stats_core import get_user_stats

from .component_building import build_linked_quests_listing_components, build_quest_board_quest_listing_components


async def command_guild_quest_board(client, interaction_event):
    """
    Shows the guild's quest board.
        
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    guild = interaction_event.guild
    if (guild is None):
        return
    
    await client.application_command_acknowledge(
        interaction_event,
        False,
    )
    user_id = interaction_event.user_id
    
    guild_stats = await get_guild_stats(guild.id)
    user_stats = await get_user_stats(user_id)
    linked_quest_listing = await get_linked_quest_listing(user_id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_quest_board_quest_listing_components(
            guild, guild_stats, user_stats, linked_quest_listing, 0
        ),
    )


async def command_user_quests(client, interaction_event):
    """
    Lists your accepted quests.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user : ``ClientUserbase``
        The respective user.
    
    guild_id : `int`
        The guild identifier the command is called from.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    await client.application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user_id = interaction_event.user_id
    linked_quest_listing = await get_linked_quest_listing(user_id)
    user_stats = await get_user_stats(user_id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_linked_quests_listing_components(
            interaction_event.user, interaction_event.guild_id, user_stats, linked_quest_listing, 0
        )
    )
