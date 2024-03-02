__all__ = ('build_notification_settings_embed',)

from hata import CLIENTS, Embed

from .constants import NOTIFIER_NAME_DEFAULT
from .options import NOTIFICATION_SETTINGS_SORTED


def build_notification_settings_change_description(option, value, changed):
    """
    Builds notification change description.
    
    Parameters
    ----------
    option : ``NotificationOption``
        Option representing the changed notification setting.
    value : `bool`
        The new value to set.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    description : `str`
    """
    long_name = option.long_name
    
    if changed:
        if value:
            description = f'From now on, you will receive {long_name} notifications.'
        else:
            description = f'From now, you will **not** receive {long_name} notifications.'
    else:
        if value:
            description = f'You were already receiving {long_name} notifications.'
        else:
            description = f'You were already **not** receiving {long_name} notifications.'
        
    return description


def build_notification_settings_change_embed(user, option, value, changed):
    """
    Builds notification change embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's notification settings are changed.
    option : ``NotificationOption``
        Option representing the changed notification setting.
    value : `bool`
        The new value to set.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        ('Great success!' if changed else 'Uoh'),
        build_notification_settings_change_description(option, value, changed),
    ).add_thumbnail(
        user.avatar_url,
    )


def build_notification_settings_notifier_change_description(client, hit, changed):
    """
    Builds notification settings notifier change description.
    
    Parameters
    ----------
    client : `None | ClientUserBase`
        The client the notification settings were set to.
    hit : `bool`
        Whether a client option was hit by the user's input.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    description : `str`
    """
    if not hit:
        description = 'Could not match any available clients.'
    
    else:
        if client is None:
            client_name = NOTIFIER_NAME_DEFAULT
        else:
            client_name = client.full_name
        
        if changed:
            description = f'Notifier set to `{client_name!s}`.'
        else:
            description = f'Notifier was already `{client_name!s}`.'
    
    return description


def build_notification_settings_notifier_change_embed(user, client, hit, changed):
    """
    Builds a notification settings notifier change embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's notification settings are changed.
    client : `None | ClientUserBase`
        The client the notification settings were set to.
    hit : `bool`
        Whether a client option was hit by the user's input.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    embed : ``Embed``
    """
    return Embed(
        ('Great success!' if changed else 'Uoh'),
        build_notification_settings_notifier_change_description(client, hit, changed),
    ).add_thumbnail(
        user.avatar_url,
    )


def build_notification_settings_embed(user, notification_settings):
    """
    Builds notification settings embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    notification_settings : ``NotificationSettings``
        The user's notification settings.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Notification settings',
    ).add_thumbnail(
        user.avatar_url,
    )
    
    notifier_client_id = notification_settings.notifier_client_id
    if notifier_client_id:
        notifier_client = CLIENTS.get(notifier_client_id, None)
    else:
        notifier_client = None
    
    embed.add_field(
        'Notifier',
        (
            f'```\n'
            f'{NOTIFIER_NAME_DEFAULT if notifier_client is None else notifier_client.full_name!s}\n'
            f'```'
        )
    )
    
    for option in NOTIFICATION_SETTINGS_SORTED:
        value = option.get(notification_settings)
        
        embed.add_field(
            option.long_name.capitalize(),
            (
                f'```\n'
                f'{"true" if value else "false"!s}\n'
                f'```'
            )
        )
    
    return embed
