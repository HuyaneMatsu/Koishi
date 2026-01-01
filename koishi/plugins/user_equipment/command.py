__all__ = ('command_user_equipment',)

from hata import ClientUserBase

from ..user_stats_core import get_user_stats

from .component_building import build_user_equipment_components


async def command_user_equipment(
    client,
    interaction_event,
    user: (ClientUserBase, 'Select someone else?') = None,
):
    """
    Shows your equipment.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        the client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user : ``None | ClientUserBase`` = `None`, Optional
        The selected user.
    """
    if user is None:
        user = interaction_event.user
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    stats = await get_user_stats(user.id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_user_equipment_components(user, stats, interaction_event.guild_id),
    )
