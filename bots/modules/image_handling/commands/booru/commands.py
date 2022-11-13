__all__ = ()

import re

from hata import Client
from hata.ext.slash import abort

from .booru import (
    CACHES, CUSTOM_ID_NEW_DISABLED, CUSTOM_ID_TAGS_DISABLED, ImageCache, SESSION_ID, build_booru_disabled_components,
    build_tag_embed
)


SLASH_CLIENT: Client


@SLASH_CLIENT.interactions(is_global = True)
async def safe_booru(
    client,
    event,
    tags: ('str', 'Some tags to spice it up?') = '',
):
    """Some safe images?"""
    if not event.guild_id:
        abort(f'Guild only command.')
    
    cache = ImageCache(True, tags)
    await cache.invoke_initial(client, event)


@SLASH_CLIENT.interactions(is_global = True, nsfw = True)
async def nsfw_booru(
    client,
    event,
    tags: ('str', 'Some tags to spice it up?') = '',
):
    """Some not so safe images? You perv!"""
    if not event.guild_id:
        abort(f'Guild only command.')
    
    if (not event.channel.nsfw):
        if 'koishi' in tags.lower():
            description = 'I love you too\~,\nbut this is not the right place to lewd.'
        else:
            description = 'Onii chaan\~,\nthis is not the right place to lewd.'
        
        abort(description)
    
    cache = ImageCache(False, tags)
    await cache.invoke_initial(client, event)


@SLASH_CLIENT.interactions(custom_id = [CUSTOM_ID_NEW_DISABLED, CUSTOM_ID_TAGS_DISABLED])
async def booru_disabled():
    pass


async def notify_session_expiration(client, event):
    """
    Notifies the user about the expired session.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        the client who received the interaction.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_message_edit(
        event,
        components = build_booru_disabled_components(),
    )
    
    await client.interaction_followup_message_create(
        event,
        content = 'Session expired',
        show_for_invoking_user_only = True,
    )


@SLASH_CLIENT.interactions(custom_id = re.compile('booru\.(\d+)\.(\d+)\.new'))
async def booru_new(client, event, session_id, cache_id):
    if event.user is not event.message.interaction.user:
        return
    
    session_id = int(session_id)
    if session_id == SESSION_ID:
        cache_id = int(cache_id)
        try:
            cache = CACHES[cache_id]
        except KeyError:
            pass
        else:
            await cache.invoke_continuous(client, event)
            return
    
    await notify_session_expiration(client, event)


@SLASH_CLIENT.interactions(custom_id = re.compile('booru\.(\d+)\.(\d+)\.tags'))
async def booru_tags(client, event, session_id, cache_id):
    session_id = int(session_id)
    if session_id == SESSION_ID:
        cache_id = int(cache_id)
        try:
            cache = CACHES[cache_id]
        except KeyError:
            pass
        else:
            await client.interaction_response_message_create(
                event,
                embed = build_tag_embed(cache.last),
                show_for_invoking_user_only = True,
            )
            return
    
    await notify_session_expiration(client, event)
