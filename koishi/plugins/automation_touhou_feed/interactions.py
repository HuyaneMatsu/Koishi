__all__ = ()

from re import compile as re_compile, escape as re_escape

from ...bots import FEATURE_CLIENTS

from ..automation_core import get_touhou_feed_enabled

from .commands_core import (
    build_touhou_feed_listing_response, create_about_examples, create_about_interval, create_about_main
)
from .constants import (
    CUSTOM_ID_ABOUT_EXAMPLES, CUSTOM_ID_ABOUT_INTERVAL, CUSTOM_ID_ABOUT_MAIN, CUSTOM_ID_CLOSE, CUSTOM_ID_PAGE_BASE,
    CUSTOM_ID_PAGE_NEXT_DISABLED, CUSTOM_ID_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_REFRESH_BASE
)

# ---- about ----

@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ABOUT_MAIN)
async def response_about_main(client, event):
    """
    Handles `about.main` component click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.user is event.message.interaction.user:
        return create_about_main(client, event)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ABOUT_EXAMPLES)
async def response_about_examples(client, event):
    """
    Handles `about.examples` component click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.user is event.message.interaction.user:
        return create_about_examples(client, event)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_ABOUT_INTERVAL)
async def response_about_interval(client, event):
    """
    Handles `about.interval` component click.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if event.user is event.message.interaction.user:
        return create_about_interval(client, event)


# ---- listing ----

@FEATURE_CLIENTS.interactions(custom_id = [CUSTOM_ID_PAGE_PREVIOUS_DISABLED, CUSTOM_ID_PAGE_NEXT_DISABLED])
async def disabled_page_move():
    """
    Called when a disabled page-move is clicked. Does nothing.
    
    This function is a coroutine.
    """
    pass


@FEATURE_CLIENTS.interactions(custom_id = re_compile(re_escape(CUSTOM_ID_PAGE_BASE) + '(\d+)'))
async def page_move(client, event, page):
    """
    Called when a disabled page-move is clicked. Does nothing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    page : `str`
        The selected page. Later converted to integer.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    guild = event.guild
    if (guild is not None) and event.user_permissions.can_administrator:
        return build_touhou_feed_listing_response(client, guild, int(page), get_touhou_feed_enabled(guild.id))


@FEATURE_CLIENTS.interactions(custom_id = re_compile(re_escape(CUSTOM_ID_REFRESH_BASE) + '(\d+)'))
async def page_refresh(client, event, page):
    """
    Refreshes the current page.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    page : `str`
        The currently selected page. Later converted to integer.
    
    Returns
    -------
    response : `None`, ``InteractionResponse``
    """
    guild = event.guild
    if (guild is not None) and event.user_permissions.can_administrator:
        return build_touhou_feed_listing_response(client, guild, int(page), get_touhou_feed_enabled(guild.id))


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_CLOSE)
async def close_message(client, event):
    """
    Closes the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received event.
    """
    if event.user_permissions.can_manage_messages:
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)
