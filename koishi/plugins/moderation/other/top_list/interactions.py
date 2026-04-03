__all__ = ()

from hata import Client
from hata.ext.slash import P

from ..helpers import (
    check_required_permissions_only_client, check_required_permissions_only_guild, check_required_permissions_only_user
)

from .builders import build_top_list_response
from .constants import (
    DAYS_MAX, DAYS_MIN, PAGE_MAX, PAGE_MIN, REQUIRED_PERMISSIONS_CLIENT_NAME, REQUIRED_PERMISSIONS_CLIENT_VALUE,
    REQUIRED_PERMISSIONS_USER_NAME, REQUIRED_PERMISSIONS_USER_VALUE, TYPES, TYPE_ALL
)
from .queries import request_top_list


def check_required_top_list_permissions(client, event, guild):
    """
    Checks whether the user and the client has enough permissions to invoke the `top-list` command.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    guild : ``Guild``
        The guild to request the actions at.
    """
    check_required_permissions_only_guild(guild)
    check_required_permissions_only_user(event, REQUIRED_PERMISSIONS_USER_VALUE, REQUIRED_PERMISSIONS_USER_NAME)
    check_required_permissions_only_client(
        client, guild, REQUIRED_PERMISSIONS_CLIENT_VALUE, REQUIRED_PERMISSIONS_CLIENT_NAME
    )


async def top_list_command(
    client,
    event,
    sort_by : (TYPES, 'Specific action type to sort by.') = TYPE_ALL,
    days : P(int, 'The days to get.', min_value = DAYS_MIN, max_value = DAYS_MAX) = DAYS_MAX,
    page : P(int, 'Page to get..', min_value = PAGE_MIN + 1, max_value = PAGE_MAX + 1) = PAGE_MIN + 1,
):
    """
    Shows mod top-list.
    
    This function is a coroutine generator.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    sort_by : `int` = `TYPE_ALL`, Optional
        The actions' identifier to sort by.
    days : `int` = `DAYS_MAX`, Optional
        The days to request.
    page : `int` = `PAGE_MIN`, Optional
        The page to show. (1 based.)
    
    Yields
    ------
    acknowledge / response : `None`, ``InteractionResponse``
    """
    guild = event.guild
    check_required_top_list_permissions(client, event, guild)
    yield
    entries = await request_top_list(client, guild, sort_by, days)
    yield build_top_list_response(page - 1, entries, sort_by, days)


async def top_list_command_component_close(client, event):
    """
    Deletes the top-list message if the user has enough permissions.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    """
    permissions = event.user_permissions
    if (
        permissions.manage_messages or
        permissions & REQUIRED_PERMISSIONS_USER_VALUE == REQUIRED_PERMISSIONS_USER_VALUE
    ):
        await client.interaction_component_acknowledge(event)
        await client.interaction_response_message_delete(event)


async def top_list_command_component_page(client, event, page_index, sort_by, days):
    """
    Changes the page of the top-list.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    page_index : `str`
        The page to show. Later converted to `int`. (0 based.)
    sort_by : `str`
        The actions' identifier to sort by. Later converted to `int`.
    days : `str`
        The days to request. Later converted to `int`.
    
    Yields
    ------
    acknowledge / response : `None`, ``InteractionResponse``
    """
    page_index = int(page_index)
    sort_by = int(sort_by)
    days = int(days)
    
    guild = event.guild
    check_required_top_list_permissions(client, event, guild)
    yield
    entries = await request_top_list(client, guild, sort_by, days)
    yield build_top_list_response(page_index, entries, sort_by, days)
