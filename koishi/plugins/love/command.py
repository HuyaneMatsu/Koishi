__all__ = ()

from hata import Embed, BUILTIN_EMOJIS
from hata.ext.slash import abort

from ...bots import FEATURE_CLIENTS

from ..relationships_core import get_affinity_percent

from .love_options import LOVE_OPTIONS


@FEATURE_CLIENTS.interactions(is_global = True)
async def love(
    client,
    event,
    user_0: ('user', 'Select your heart\'s chosen one!', 'user') = None,
    user_1: ('user', 'Check some else\'s love life?', 'with') = None,
):
    """
    How much you two fit together?
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the vent.
    
    event : ``InteractionEvent``
        The received event.
    
    user_0 : `None | ClientUserBase` = `None`, Optional
        Selected user.
    
    user_1 : `None | ClientUserBase` = `None`, Optional
        Selected user.
    
    Returns
    -------
    response : ``Embed``
    """
    if user_1 is None:
        source_user = event.user
        
        if user_0 is None:
            target_user = client
        else:
            target_user = user_0
    else:
        target_user = user_1
        
        if user_0 is None:
            source_user = event.user
        else:
            source_user = user_0
    
    if source_user is target_user:
        abort('huh?')
    
    source_user_id = source_user.id
    target_user_id = target_user.id
    percent = get_affinity_percent(source_user_id, target_user_id)
    love_option = LOVE_OPTIONS[percent]
    
    title_seed = source_user_id ^ target_user_id
    titles = love_option.titles
    title = titles[title_seed % len(titles)]
    
    return Embed(
        title,
        (
            f'{source_user.name_at(event.guild_id)} {BUILTIN_EMOJIS["heart"]} {target_user.name_at(event.guild_id)} '
            f'scored {percent}%!'
        ),
        color = 0xad1457,
    ).add_field(
        'My advice:',
        love_option.text,
    )
