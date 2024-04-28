__all__ = (
    'autocomplete_user_settings_preferred_client', 'handle_user_settings_change',
    'handle_user_settings_set_preferred_client', 'handle_user_settings_set_preferred_image_source',
    'get_preferred_client_for_user', 'get_preferred_client_in_channel',
    'get_preferred_image_source_weight_map', 'is_preferred_image_source_weight_map_valuable',
)

from hata import CLIENTS, Permission
from hata.ext.slash import InteractionResponse

from ...bots import FEATURE_CLIENTS, MAIN_CLIENT

from .constants import PREFERRED_CLIENT_NAME_DEFAULT, PREFERRED_IMAGE_SOURCE_NAMES, PREFERRED_IMAGE_SOURCE_NONE
from .builders import (
    build_user_settings_notification_change_embed, build_user_settings_preferred_client_change_embed,
    build_user_settings_preferred_image_source_change_embed,
)
from .options import OPTION_PREFERRED_CLIENT_ID, OPTION_PREFERRED_IMAGE_SOURCE
from .queries import get_one_user_settings, get_more_user_settings, save_one_user_settings


PERMISSION_MASK_MESSAGING__DEFAULT = Permission().update_by_keys(
    send_messages = True,
)

PERMISSION_MASK_MESSAGING__THREAD = Permission().update_by_keys(
    send_messages_in_threads = True,
)


async def set_user_settings_option(user_settings, option, value):
    """
    Sets a user settings option to the given value.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user settings to modify.
    option : ``UserSettingsOption``
        Its option to modify.
    value : `bool`
        The value to set.
    
    Returns
    -------
    changed : `bool`
    """
    actual = option.get(user_settings)
    if actual == value:
        return False
    
    option.set(user_settings, value)
    await save_one_user_settings(user_settings)
    return True


async def handle_user_settings_change(event, option, value):
    """
    handles a user settings change.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    option : ``NotificationOption``
        Option representing the changed user setting.
    value : `bool`
        The new value to set.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    user_settings = await get_one_user_settings(event.user.id)
    changed = await set_user_settings_option(user_settings, option, value)
    return InteractionResponse(
        embed = build_user_settings_notification_change_embed(event.user, option, value, changed),
        show_for_invoking_user_only = True,
    )


def get_available_clients(user):
    """
    Gets the available clients for the user.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user to get the clients for.
    
    Returns
    -------
    clients : `set<Client>`
    """
    clients = set()
    for guild in user.iter_guilds():
        clients.update(guild.clients)
    
    return clients.intersection(FEATURE_CLIENTS.clients)


def get_preferred_client_for_user(user, preferred_client_id, default_client):
    """
    Gets the preferred client for the given user.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user of whom to get their user settings of.
    preferred_client_id : `int`
        The client's identifier to get.
    default_client : `None | Client`
        Client to return if no client is set.
    
    Returns
    -------
    client : ``Client``
    """
    if preferred_client_id:
        try:
            client = CLIENTS[preferred_client_id]
        except KeyError:
            pass
        else:
            return client
    
    if (default_client is not None):
        return default_client
    
    available_clients = get_available_clients(user)
    if available_clients:
        return next(iter(available_clients))
    
    return MAIN_CLIENT


def get_preferred_client_in_channel(channel, preferred_client_id, default_client, extra = 0):
    """
    Gets the preferred client for in the given channel.
    Only checks `preferred_client_id` and `default_client`, ignores others.
    
    Parameters
    ----------
    chanel : ``Channel``
        Channel to check the client's permissions in.
    preferred_client_id : `int`
        The client's identifier to get.
    default_client : `None | Client`
        Client to return if no client is set.
    extra : `int` = `0`, Optional
        Additional permissions to check for.
    
    Returns
    -------
    client : `None`, ``Client``
        Can return `None` only if `default_client` is `None`.
    """
    if not preferred_client_id:
        return default_client
    
    try:
        client = CLIENTS[preferred_client_id]
    except KeyError:
        return default_client
    
    if channel.is_in_group_thread():
        mask = PERMISSION_MASK_MESSAGING__THREAD
    else:
        mask = PERMISSION_MASK_MESSAGING__DEFAULT
    
    mask |= extra
    
    if channel.cached_permissions_for(client) & mask != mask:
        return default_client
    
    return client


async def autocomplete_user_settings_preferred_client(event, value):
    """
    Auto completer for user setting preferred client.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    value : `None | str`
        Value provided by the user.
    
    This function is a coroutine.
    
    Returns
    -------
    suggestions : `list<str>`
    """
    clients = get_available_clients(event.user)
    client_names = [client.full_name for client in clients]
    if value is None:
        insert_unset = True
    
    else:
        value = value.casefold()
        client_names = [client_name for client_name in client_names if value in client_name.casefold()]
        insert_unset = value in PREFERRED_CLIENT_NAME_DEFAULT
    
    client_names.sort()
    
    if insert_unset:
        client_names.insert(0, PREFERRED_CLIENT_NAME_DEFAULT)
    
    return client_names


def _clients_sort_key(client):
    """
    Sort key used to sort clients by their name,
    
    Parameters
    ----------
    client : ``Client``
        Client to get its sort key of.
    
    Returns
    -------
    sort_key : `str`
    """
    return client.full_name


def get_user_settings_preferred_client(event, value):
    """
    Gets the preferred client for the given event.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    value : `str`
        The value provided by the user.
    
    Returns
    -------
    hit : `bool`
    client : `None | Client`
    """
    if not value:
        return True, None
    
    value = value.casefold()
    if value in PREFERRED_CLIENT_NAME_DEFAULT:
        return True, None
    
    clients = get_available_clients(event.user)
    for client in sorted(clients, key = _clients_sort_key):
        if value in client.full_name.casefold():
            return True, client
    
    return False, None


async def handle_user_settings_set_preferred_client(event, value):
    """
    Handles a set preferred client.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    value : `str`
        The new value to set.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    hit, client = get_user_settings_preferred_client(event, value)
    if not hit:
        changed = False
    
    else:
        user_settings = await get_one_user_settings(event.user.id)
        changed = await set_user_settings_option(
            user_settings,
            OPTION_PREFERRED_CLIENT_ID,
            0 if client is None else client.id,
        )

    return InteractionResponse(
        embed = build_user_settings_preferred_client_change_embed(event.user, client, hit, changed),
        show_for_invoking_user_only = True,
    )


async def handle_user_settings_set_preferred_image_source(event, value):
    """
    Handles a set preferred image source.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    value : `int`
        The new value to set.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    if value in PREFERRED_IMAGE_SOURCE_NAMES.keys():
        hit = True
        user_settings = await get_one_user_settings(event.user.id)
        changed = await set_user_settings_option(
            user_settings,
            OPTION_PREFERRED_IMAGE_SOURCE,
            value,
        )
        
    else:
        hit = False
        changed = False
    
    return InteractionResponse(
        embed = build_user_settings_preferred_image_source_change_embed(event.user, value, hit, changed),
        show_for_invoking_user_only = True,
    )


async def get_preferred_image_source_weight_map(user_ids):
    """
    Gets an preferred image source weight table for the given users..
    
    Parameters
    ----------
    user_ids : `list<int>`
        User identifiers to get weights for.
    
    Returns
    -------
    preferred_image_source_weight_map : `dict<int, int>`
    """
    user_settings = await get_more_user_settings(user_ids)
    
    preferred_image_source_weight_map = {}
    for user_setting in user_settings:
        preferred_image_source = user_setting.preferred_image_source
        preferred_image_source_weight_map[preferred_image_source] = (
            preferred_image_source_weight_map.get(preferred_image_source, 0.0) + 1.0
        )
    
    return preferred_image_source_weight_map


def is_preferred_image_source_weight_map_valuable(preferred_image_source_weight_map):
    """
    Whether the information stored inside of the preferred image source wight map is valuable.
    
    Parameters
    ----------
    preferred_image_source_weight_map : `dict<int, int>`
        Weight map.
    
    Returns
    -------
    is_valuable : `int`
    """
    return (
        len(preferred_image_source_weight_map) -
        (PREFERRED_IMAGE_SOURCE_NONE in preferred_image_source_weight_map.keys())
    )
