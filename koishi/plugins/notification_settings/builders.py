__all__ = ('build_notification_settings_embed',)

from hata import Embed

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
    
    for option in NOTIFICATION_SETTINGS_SORTED:
        value = option.get(notification_settings)
        
        embed.add_field(
            option.long_name.capitalize(),
            (
                f'```\n'
                f'{"true" if value else "false"}\n'
                f'```'
            )
        )
    
    return embed
