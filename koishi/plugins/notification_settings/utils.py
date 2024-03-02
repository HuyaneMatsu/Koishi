__all__ = (
    'autocomplete_notification_settings_notifier', 'handle_notification_settings_change',
    'handle_notification_settings_set_notifier', 'get_notifier_client',
)

from hata import CLIENTS
from hata.ext.slash import InteractionResponse

from ...bots import FEATURE_CLIENTS, MAIN_CLIENT

from .constants import NOTIFIER_NAME_DEFAULT
from .builders import build_notification_settings_change_embed, build_notification_settings_notifier_change_embed
from .options import OPTION_NOTIFIER_CLIENT_ID
from .queries import get_one_notification_settings, save_one_notification_settings


async def set_notification_settings_option(notification_settings, option, value):
    """
    Sets a notification settings option to the given value.
    
    Parameters
    ----------
    notification_settings : ``NotificationSettings``
        The notification settings to modify.
    option : ``NotificationSettingsOption``
        Its option to modify.
    value : `bool`
        The value to set.
    
    Returns
    -------
    changed : `bool`
    """
    actual = option.get(notification_settings)
    if actual == value:
        return False
    
    option.set(notification_settings, value)
    await save_one_notification_settings(notification_settings)
    return True


async def handle_notification_settings_change(event, option, value):
    """
    handles a notification settings change.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    option : ``NotificationOption``
        Option representing the changed notification setting.
    value : `bool`
        The new value to set.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    notification_settings = await get_one_notification_settings(event.user.id)
    changed = await set_notification_settings_option(notification_settings, option, value)
    return InteractionResponse(
        embed = build_notification_settings_change_embed(event.user, option, value, changed),
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


def get_notifier_client(user, notifier_client_id, default_client):
    """
    Gets the notifier client for the given user.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user of whom to get their notification settings of.
    notifier_client_id : `int`
        The client's identifier to get.
    default_client : `None | Client`
        Client to return if no client is set.
    
    Returns
    -------
    client : ``Client``
    """
    if notifier_client_id:
        try:
            client = CLIENTS[notifier_client_id]
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


async def autocomplete_notification_settings_notifier(event, value):
    """
    Auto completer for notification setting notifier.
    
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
        insert_unset = value in NOTIFIER_NAME_DEFAULT
    
    client_names.sort()
    
    if insert_unset:
        client_names.insert(0, NOTIFIER_NAME_DEFAULT)
    
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


def get_notification_settings_notifier(event, value):
    """
    Gets the notifier for the given event.
    
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
    if value in NOTIFIER_NAME_DEFAULT:
        return True, None
    
    clients = get_available_clients(event.user)
    for client in sorted(clients, key = _clients_sort_key):
        if value in client.full_name.casefold():
            return True, client
    
    return False, None


async def handle_notification_settings_set_notifier(event, value):
    """
    Handles a set notifier.
    
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
    hit, client = get_notification_settings_notifier(event, value)
    if not hit:
        changed = False
    
    else:
        notification_settings = await get_one_notification_settings(event.user.id)
        changed = await set_notification_settings_option(
            notification_settings,
            OPTION_NOTIFIER_CLIENT_ID,
            0 if client is None else client.id,
        )

    return InteractionResponse(
        embed = build_notification_settings_notifier_change_embed(event.user, client, hit, changed),
        show_for_invoking_user_only = True,
    )
