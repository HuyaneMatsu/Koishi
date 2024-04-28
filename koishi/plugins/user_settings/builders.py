__all__ = ('build_notification_settings_embed', 'build_preference_settings_embed')

from hata import CLIENTS, Embed

from .constants import PREFERRED_IMAGE_SOURCE_NAME_DEFAULT, PREFERRED_IMAGE_SOURCE_NAMES, PREFERRED_CLIENT_NAME_DEFAULT
from .options import NOTIFICATION_SETTINGS_SORTED


def build_user_settings_notification_change_description(option, value, changed):
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


def build_user_settings_notification_change_embed(user, option, value, changed):
    """
    Builds notification change embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's user settings are changed.
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
        build_user_settings_notification_change_description(option, value, changed),
    ).add_thumbnail(
        user.avatar_url,
    )


def build_user_settings_preferred_client_change_description(client, hit, changed):
    """
    Builds user settings preferred client change description.
    
    Parameters
    ----------
    client : `None | ClientUserBase`
        The preferred client that were set.
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
            client_name = PREFERRED_CLIENT_NAME_DEFAULT
        else:
            client_name = client.full_name
        
        if changed:
            description = f'Preferred client set to `{client_name!s}`.'
        else:
            description = f'Preferred client was already `{client_name!s}`.'
    
    return description


def build_user_settings_preferred_client_change_embed(user, client, hit, changed):
    """
    Builds a user settings preferred client change embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's user settings are changed.
    client : `None | ClientUserBase`
        The client who were set as preferred client.
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
        build_user_settings_preferred_client_change_description(client, hit, changed),
    ).add_thumbnail(
        user.avatar_url,
    )


def build_user_settings_preferred_image_source_change_description(preferred_image_source, hit, changed):
    """
    Builds user settings preferred image source change description.
    
    Parameters
    ----------
    preferred_image_source : `int`
        The preferred image source that were set.
    hit : `bool`
        Whether a client option was hit by the user's input.
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    description : `str`
    """
    if not hit:
        description = 'Could not match any preferred image source.'
    
    else:
        preferred_image_source_name = PREFERRED_IMAGE_SOURCE_NAMES.get(
            preferred_image_source, PREFERRED_IMAGE_SOURCE_NAME_DEFAULT
        )
        if changed:
            description = f'Preferred image source set to `{preferred_image_source_name!s}`.'
        else:
            description = f'Preferred image source was already `{preferred_image_source_name!s}`.'
    
    return description


def build_user_settings_preferred_image_source_change_embed(user, preferred_image_source, hit, changed):
    """
    Builds a user settings preferred image source change embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's user settings are changed.
    preferred_image_source : `int`
        The preferred image source that were set.
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
        build_user_settings_preferred_image_source_change_description(preferred_image_source, hit, changed),
    ).add_thumbnail(
        user.avatar_url,
    )


def build_notification_settings_embed(user, user_settings):
    """
    Builds user settings embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    user_settings : ``UserSettings``
        The user's settings.
    
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
        value = option.get(user_settings)
        
        embed.add_field(
            option.long_name.capitalize(),
            (
                f'```\n'
                f'{"true" if value else "false"!s}\n'
                f'```'
            )
        )
    
    return embed


def build_preference_settings_embed(user, user_settings):
    """
    Builds preference settings embed.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The respective user.
    user_settings : ``UserSettings``
        The user's settings.
    
    Returns
    -------
    embed : ``Embed``
    """
    embed = Embed(
        'Preference settings',
    ).add_thumbnail(
        user.avatar_url,
    )
    
    # preferred_client_id
    preferred_client_id = user_settings.preferred_client_id
    if preferred_client_id:
        preferred_client = CLIENTS.get(preferred_client_id, None)
    else:
        preferred_client = None
    
    embed.add_field(
        'Preferred client',
        (
            f'```\n'
            f'{PREFERRED_CLIENT_NAME_DEFAULT if preferred_client is None else preferred_client.full_name!s}\n'
            f'```'
        )
    )
    
    # preferred_image_source
    preferred_image_source_name = PREFERRED_IMAGE_SOURCE_NAMES.get(
        user_settings.preferred_image_source, PREFERRED_IMAGE_SOURCE_NAME_DEFAULT
    )
    embed.add_field(
        'Preferred image source',
        (
            f'```\n'
            f'{preferred_image_source_name!s}\n'
            f'```'
        )
    )
    
    return embed
