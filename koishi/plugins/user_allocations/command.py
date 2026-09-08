__all__ = ('command_user_allocations',)

from ..user_balance import user_balance_get, user_balance_iter_allocations

from .component_building import build_view_components
from .constants import PAGE_SIZE


async def command_user_allocations(
    client,
    interaction_event,
):
    """
    Shows the places where the user's balance is currently being allocated at.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
    )
    
    user_balance = await user_balance_get(interaction_event.user_id)
    allocations = [*user_balance_iter_allocations(user_balance)]
    page_count = (len(allocations) + PAGE_SIZE - 1) // PAGE_SIZE
    allocations_page = allocations[0 : PAGE_SIZE]
    
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_view_components(
            interaction_event.user, 0, page_count, interaction_event.guild_id, allocations_page
        ),
    )
    return
