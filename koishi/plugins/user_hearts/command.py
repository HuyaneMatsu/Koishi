__all__ = ('user_hearts_command', )


from hata import ClientUserBase
from hata.ext.slash import InteractionResponse, abort

from .response_builders import HEARTS_FIELD_CHOICES, HEARTS_FIELD_NAME_TO_RESPONSE_BUILDER, HEARTS_FIELD_NAME_SHORT


async def user_hearts_command(
    interaction_event,
    target_user: (ClientUserBase, 'Do you wanna know some1 else\'s hearts?') = None,
    field: (HEARTS_FIELD_CHOICES, 'Choose a field!') = HEARTS_FIELD_NAME_SHORT,
):
    """
    How many hearts do you have?
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target_user : `None | ClientUserBase`
        The targeted user.
    
    field : `str`
        The field to show.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if target_user is None:
        target_user = interaction_event.user
    
    try:
        response_builder = HEARTS_FIELD_NAME_TO_RESPONSE_BUILDER[field]
    except KeyError:
        return abort(f'Unknown field: {field!r}.')
    
    return await response_builder(interaction_event, target_user)
