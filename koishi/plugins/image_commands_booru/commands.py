__all__ = ()

import re

from hata import Client
from hata.ext.slash import abort

from ...bots import FEATURE_CLIENTS

from .booru import (
    CACHES, CUSTOM_ID_NEW_DISABLED, CUSTOM_ID_TAGS_DISABLED, ImageCache, SESSION_ID, build_booru_disabled_components,
    build_tag_embed
)
from .constants import AUTOCOMPLETE_VALUE_LENGTH_MAX, CUSTOM_ID_CLOSE
from .helpers import iter_split_tags_safe_booru, iter_split_tags_gel_booru, split_down_full_tags, split_tags
from .parsers import event_user_matches, parse_image_url
from .tag_cache import get_tag_auto_completion


TAG_DESCRIPTION = 'Some tags to spice it up?'


@FEATURE_CLIENTS.interactions(is_global = True, name = 'safebooru')
async def safe_booru(
    client,
    event,
    tag_00: (str, TAG_DESCRIPTION, 'tag-1' ) = None,
    tag_01: (str, TAG_DESCRIPTION, 'tag-2' ) = None,
    tag_02: (str, TAG_DESCRIPTION, 'tag-3' ) = None,
    tag_03: (str, TAG_DESCRIPTION, 'tag-4' ) = None,
    tag_04: (str, TAG_DESCRIPTION, 'tag-5' ) = None,
    tag_05: (str, TAG_DESCRIPTION, 'tag-6' ) = None,
    tag_06: (str, TAG_DESCRIPTION, 'tag-7' ) = None,
    tag_07: (str, TAG_DESCRIPTION, 'tag-8' ) = None,
    tag_08: (str, TAG_DESCRIPTION, 'tag-9' ) = None,
    tag_09: (str, TAG_DESCRIPTION, 'tag-10') = None,
    tag_10: (str, TAG_DESCRIPTION, 'tag-11') = None,
    tag_11: (str, TAG_DESCRIPTION, 'tag-12') = None,
    tag_12: (str, TAG_DESCRIPTION, 'tag-13') = None,
    tag_13: (str, TAG_DESCRIPTION, 'tag-14') = None,
    tag_14: (str, TAG_DESCRIPTION, 'tag-15') = None,
    tag_15: (str, TAG_DESCRIPTION, 'tag-16') = None,
    tag_16: (str, TAG_DESCRIPTION, 'tag-17') = None,
    tag_17: (str, TAG_DESCRIPTION, 'tag-18') = None,
    tag_18: (str, TAG_DESCRIPTION, 'tag-19') = None,
    tag_19: (str, TAG_DESCRIPTION, 'tag-20') = None,
    tag_20: (str, TAG_DESCRIPTION, 'tag-21') = None,
    tag_21: (str, TAG_DESCRIPTION, 'tag-22') = None,
    tag_22: (str, TAG_DESCRIPTION, 'tag-23') = None,
    tag_23: (str, TAG_DESCRIPTION, 'tag-24') = None,
    tag_24: (str, TAG_DESCRIPTION, 'tag-25') = None,
):
    """Some safe images?"""
    if not event.guild_id:
        abort('Guild only command.')
    
    tags = split_tags(
        [
            tag_00, tag_01, tag_02, tag_03, tag_04, tag_05, tag_06, tag_07, tag_07, tag_08, tag_09,
            tag_10, tag_11, tag_12, tag_13, tag_14, tag_15, tag_16, tag_17, tag_17, tag_18, tag_19,
            tag_20, tag_21, tag_22, tag_23, tag_24
        ],
        True,
    )
    cache = ImageCache({(True, tag) for tag in tags}, True)
    await cache.invoke_initial(client, event)


@FEATURE_CLIENTS.interactions(is_global = True, nsfw = True, name = 'nsfwbooru')
async def nsfw_booru(
    client,
    event,
    tag_00: (str, TAG_DESCRIPTION, 'tag-1' ) = None,
    tag_01: (str, TAG_DESCRIPTION, 'tag-2' ) = None,
    tag_02: (str, TAG_DESCRIPTION, 'tag-3' ) = None,
    tag_03: (str, TAG_DESCRIPTION, 'tag-4' ) = None,
    tag_04: (str, TAG_DESCRIPTION, 'tag-5' ) = None,
    tag_05: (str, TAG_DESCRIPTION, 'tag-6' ) = None,
    tag_06: (str, TAG_DESCRIPTION, 'tag-7' ) = None,
    tag_07: (str, TAG_DESCRIPTION, 'tag-8' ) = None,
    tag_08: (str, TAG_DESCRIPTION, 'tag-9' ) = None,
    tag_09: (str, TAG_DESCRIPTION, 'tag-10') = None,
    tag_10: (str, TAG_DESCRIPTION, 'tag-11') = None,
    tag_11: (str, TAG_DESCRIPTION, 'tag-12') = None,
    tag_12: (str, TAG_DESCRIPTION, 'tag-13') = None,
    tag_13: (str, TAG_DESCRIPTION, 'tag-14') = None,
    tag_14: (str, TAG_DESCRIPTION, 'tag-15') = None,
    tag_15: (str, TAG_DESCRIPTION, 'tag-16') = None,
    tag_16: (str, TAG_DESCRIPTION, 'tag-17') = None,
    tag_17: (str, TAG_DESCRIPTION, 'tag-18') = None,
    tag_18: (str, TAG_DESCRIPTION, 'tag-19') = None,
    tag_19: (str, TAG_DESCRIPTION, 'tag-20') = None,
    tag_20: (str, TAG_DESCRIPTION, 'tag-21') = None,
    tag_21: (str, TAG_DESCRIPTION, 'tag-22') = None,
    tag_22: (str, TAG_DESCRIPTION, 'tag-23') = None,
    tag_23: (str, TAG_DESCRIPTION, 'tag-24') = None,
    tag_24: (str, TAG_DESCRIPTION, 'tag-25') = None,
):
    """Some not so safe images? You perv!"""
    if not event.guild_id:
        abort('Guild only command.')
    
    tags = split_tags(
        [
            tag_00, tag_01, tag_02, tag_03, tag_04, tag_05, tag_06, tag_07, tag_07, tag_08, tag_09,
            tag_10, tag_11, tag_12, tag_13, tag_14, tag_15, tag_16, tag_17, tag_17, tag_18, tag_19,
            tag_20, tag_21, tag_22, tag_23, tag_24
        ],
        False,
    )
    
    if len(tags) > 2:
        abort('Tag count limited to 2.')
    
    if (not event.channel.nsfw):
        if any('koishi' in tag.casefold() for tag in tags):
            description = 'I love you too\~,\nbut this is not the right place to lewd.'
        else:
            description = 'Onii chaan\~,\nthis is not the right place to lewd.'
        
        abort(description)
    
    cache = ImageCache({(True, tag) for tag in tags}, False)
    await cache.invoke_initial(client, event)


async def autocomplete_input(client, event, input_value, safe):
    """
    Auto completes the given input value.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    event : ``InteractionEvent``
        The received event.
    
    query : `str`
        The value to autocomplete.
    
    safe : `bool`
        Whether we are using safe-booru.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    if input_value is None:
        return None
    
    full_tags, input_tag = split_down_full_tags(input_value)
    if input_tag is None:
        return None
    
    excluded_tags = split_tags(event.get_non_focused_values().values(), safe)
    if (full_tags is not None):
        excluded_tags.update((iter_split_tags_safe_booru if safe else iter_split_tags_gel_booru)(full_tags))
    
    suggestions = await get_tag_auto_completion(input_tag, safe, excluded_tags)
    if (suggestions is None) or (not suggestions):
        return None
    
    if (full_tags is not None):
        suggestions = [f'{full_tags}, {tag_name}' for tag_name in suggestions]
    
    omitted = 0
    
    for index in reversed(range(len(suggestions))):
        tag_name = suggestions[index]
        if len(tag_name) > AUTOCOMPLETE_VALUE_LENGTH_MAX:
            del suggestions[index]
            omitted += 1
    
    if omitted:
        suggestions.insert(
            0,
            (
                f'... {omitted} suggestions omitted (max length) ...',
                input_value[:AUTOCOMPLETE_VALUE_LENGTH_MAX],
            ),
        )
    
    return suggestions


@safe_booru.autocomplete(*(f'tag-{index}' for index in range(25)))
async def autocomplete_safe_tags(client, event, input_value):
    """
    Auto completes the given input value. (Safe-booru completion.)
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to use to request the tags.
    event : ``InteractionEvent``
        The received event.
    query : `str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    return await autocomplete_input(client, event, input_value, True)


@nsfw_booru.autocomplete(*(f'tag-{index}' for index in range(25)))
async def autocomplete_nsfw_tags(client, event, input_value):
    """
    Auto completes the given input value. (Gel-booru completion.)
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client to use to request the tags.
    event : ``InteractionEvent``
        The received event.
    query : `str`
        The value to autocomplete.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    return await autocomplete_input(client, event, input_value, False)



@FEATURE_CLIENTS.interactions(custom_id = [CUSTOM_ID_NEW_DISABLED, CUSTOM_ID_TAGS_DISABLED])
async def booru_disabled():
    """
    Handles a disabled component click. So does nothing.
    
    This function is a coroutine.
    """
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
        components = build_booru_disabled_components(parse_image_url(event)),
    )
    
    await client.interaction_followup_message_create(
        event,
        content = 'Session expired',
        show_for_invoking_user_only = True,
    )


@FEATURE_CLIENTS.interactions(custom_id = re.compile('booru\.(\d+)\.(\d+)\.new'))
async def booru_new(client, event, session_id, cache_id):
    """
    Gets the defined cache by the parameters and responds with an another image pulled from it.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    session_id : `str`
        The current session's identifier. A new is generated on each startup. Later converted to `int`.
    cache_id : `int`
        The cache's identifier. Incremental. Later converted to `int`.
    """
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


@FEATURE_CLIENTS.interactions(custom_id = re.compile('booru\.(\d+)\.(\d+)\.tags'))
async def booru_tags(client, event, session_id, cache_id):
    """
    Gets the defined cache by the parameters and responds with the current image's tags.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    session_id : `str`
        The current session's identifier. A new is generated on each startup. Later converted to `int`.
    cache_id : `int`
        The cache's identifier. Incremental. Later converted to `int`.
    """
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


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLOSE)
async def booru_close(client, event):
    """
    Deletes the booru message if applicable.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    await client.interaction_component_acknowledge(event)
    
    if event.user_permissions.manage_messages or event_user_matches(event):
        await client.interaction_response_message_delete(event)
    
    else:
        await client.interaction_followup_message_create(
            event,
            'You must be the invoker of the interaction, or have manage messages permission to do this.',
            show_for_invoking_user_only = True,
        )
