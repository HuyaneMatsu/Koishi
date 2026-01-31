__all__ = ('command_burn_divorce_papers',)

from hata import ClientUserBase
from hata.ext.slash import P

from ..gift_common import identify_targeted_user
from ..relationships_core import autocomplete_relationship_extended_user_name

from .interactions import burn_divorce_papers_respond


async def command_burn_divorce_papers(
    client,
    interaction_event,
    target_related_name : P(
        str,
        'Hire ninjas to burn and locate divorce papers for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Hire ninjas to burn an locate divorce papers for someone else?',
        'someone-else',
    ) = None,
):
    """
    Burn divorce papers stockpiled on breakups.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    event : ``InteractionEvent``
        The received interaction event.
    
    role_choice : `str`
        The chosen role.
    
    target_related_name : `None | str` = `None`, Optional
        The targeted related user's name.
    
    target_user : ``None | ClientUserBase`` = `None`, Optional
        The targeted user.
    """
    while True:
        target_user_and_relationship_to_deepen = await identify_targeted_user(
            interaction_event.user, target_related_name, target_user, interaction_event.guild_id
        )
        
        if target_user_and_relationship_to_deepen is None:
            error_message = 'Could not match anyone.'
            break
        
        await burn_divorce_papers_respond(
            client,
            interaction_event,
            *target_user_and_relationship_to_deepen,
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
    return
