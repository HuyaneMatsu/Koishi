__all__ = ('command_user_stats',)

from hata import ClientUserBase

from ..user_stats_core import get_user_stats

from .component_building import build_user_stats_primary_components


async def command_user_stats(
    client,
    interaction_event,
    target_user: (ClientUserBase, 'Select someone else?', 'user') = None,
):
    """
    Shows your stats.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user : ``None | ClientUserBase`` = `None`, Optional
        The selected user.
    """
    if target_user is None:
        target_user = interaction_event.user
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user_stats = await get_user_stats(target_user.id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_user_stats_primary_components(
            interaction_event.user_id, target_user, user_stats, interaction_event.guild_id
        ),
    )
