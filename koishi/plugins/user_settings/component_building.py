__all__ = (
    'build_notification_settings_components', 'build_preference_settings_components', 'build_user_settings_components'
)

from hata import create_text_display

from .content_building import (
    produce_notification_change_description, produce_option_bit_listing_description,
    produce_preference_settings_description, produce_preferred_client_change_description,
    produce_preferred_image_source_change_description
)
from .options import FEATURE_SETTINGS_SORTED, NOTIFICATION_SETTINGS_SORTED


def build_notification_settings_change_components(option, value, changed):
    """
    Builds notification change components.
    
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
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_notification_change_description(option, value, changed)]),
        ),
    ]


def build_preferred_client_change_components(client, guild_id, hit, changed):
    """
    Builds a user settings preferred client change components.
    
    Parameters
    ----------
    client : ``None | ClientUserBase`
        The client who were set as prefer`red client.
    
    guild_id : `int`
        The local guild's name.
    
    hit : `bool`
        Whether a client option was hit by the user's input.
    
    changed : `bool`
        Whether value was changed.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_preferred_client_change_description(client, guild_id, hit, changed)])
        ),
    ]


def build_preferred_image_source_change_components(preferred_image_source, hit, changed):
    """
    Builds a user settings preferred image source change components.
    
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
    components : ``list<Component>``
    """
    return [
        create_text_display(
            ''.join([*produce_preferred_image_source_change_description(
                preferred_image_source, hit, changed
            )]),
        )
    ]


def build_notification_settings_components(user_settings):
    """
    Builds user settings components.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(''.join([*produce_option_bit_listing_description(
            user_settings, NOTIFICATION_SETTINGS_SORTED
        )])),
    ]


def build_preference_settings_components(user_settings, guild_id):
    """
    Builds preference settings components.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [
        create_text_display(''.join([*produce_preference_settings_description(user_settings, guild_id)])),
    ]


def build_user_settings_components(user_settings, guild_id):
    """
    Builds full user settings representation,
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    return [        
        create_text_display(''.join([*produce_option_bit_listing_description(
            user_settings, FEATURE_SETTINGS_SORTED
        )])),
        create_text_display(''.join([*produce_option_bit_listing_description(
            user_settings, NOTIFICATION_SETTINGS_SORTED
        )])),
        create_text_display(''.join([*produce_preference_settings_description(user_settings, guild_id)])),
    ]
