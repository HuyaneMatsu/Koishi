__all__ = ('command_buy_relationship_slot',)

from hata import ClientUserBase
from hata.ext.slash import P

from ..gift_common import identify_targeted_user
from ..relationships_core import autocomplete_relationship_extended_user_name

from .interactions import relationship_increment_respond


async def command_buy_relationship_slot(
    client,
    interaction_event,
    target_related_name : P(
        str,
        'Buy relationship slot for someone related',
        'related',
        autocomplete = autocomplete_relationship_extended_user_name,
    ) = None,
    target_user : (
        ClientUserBase,
        'Buy waifu slot for someone else?',
        'someone-else',
    ) = None,
):
    """
    Buy relationship slots to increase your family's size <3.
    
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
    
    target_user : `None | ClientUserBase` = `None`, Optional
        The targeted user.
    """
    target_user, relationship_to_deepen = await identify_targeted_user(
        interaction_event.user, target_related_name, target_user, interaction_event.guild_id
    )
    
    await relationship_increment_respond(
        client,
        interaction_event,
        target_user,
        relationship_to_deepen,
    )
