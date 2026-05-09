__all__ = ()

from hata import CLIENTS

from .constants import PREFERRED_IMAGE_SOURCE_NAME_DEFAULT, PREFERRED_IMAGE_SOURCE_NAMES, PREFERRED_CLIENT_NAME_DEFAULT


def produce_notification_change_description(option, value, changed):
    """
    Builds notification change description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    option : ``NotificationOption``
        Option representing the changed notification setting.
    
    value : `bool`
        The new value to set.
    
    changed : `bool`
        Whether value was changed.
    
    Yields
    ------
    part : `str`
    """
    display_name = option.display_name
    
    if changed:
        yield 'From now'
        
        if value:
            yield ' on'
        
        yield ', you will'
        
        if not value:
            yield ' **not**'
        
        yield ' receive '
    
    else:
        yield 'You were already'
        
        if not value:
            yield ' **not**'
        
        yield ' receiving '
    
    yield display_name
    yield ' notifications.'


def produce_preferred_client_change_description(client, guild_id, hit, changed):
    """
    Produces user settings preferred client change description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    client : ``None | ClientUserBase``
        The preferred client that were set.
    
    guild_id : `int`
        The local guild's name.
    
    hit : `bool`
        Whether a client option was hit by the user's input.
    
    changed : `bool`
        Whether value was changed.
    
    Yields
    ------
    part : `str`
    """
    if not hit:
        yield 'Could not match any available clients.'
        return
    
    yield 'Preferred client '
    
    yield ('set to' if changed else 'was already')
    
    if client is None:
        client_name = PREFERRED_CLIENT_NAME_DEFAULT
    else:
        client_name = client.name_at(guild_id)
    
    yield ' `'
    yield client_name
    yield '`.'


def produce_preferred_image_source_change_description(preferred_image_source, hit, changed):
    """
    Produces user settings preferred image source change description.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    preferred_image_source : `int`
        The preferred image source that were set.
    
    hit : `bool`
        Whether a client option was hit by the user's input.
    
    changed : `bool`
        Whether value was changed.
    
    Yields
    ------
    part : `str`
    """
    if not hit:
        yield 'Could not match any preferred image source.'
        return
    
    yield 'Preferred image source '
    
    yield ('set to' if changed else 'was already')
    
    yield ' `'
    yield PREFERRED_IMAGE_SOURCE_NAMES.get(preferred_image_source, PREFERRED_IMAGE_SOURCE_NAME_DEFAULT)
    yield '`.'


def produce_option_bit_listing_description(user_settings, option_bit_listing):
    """
    Produces notification settings descriptions.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    option_bit_listing : ``tuple<UserSettingsOptionBit>``
        Options to produce.
    
    Yields
    ------
    part : `str`
    """
    field_added = False
    
    for option in option_bit_listing:
        if field_added:
            yield '\n'
        else:
            field_added = True
        
        value = option.get(user_settings)
        yield '- '
        yield option.display_name.capitalize()
        yield ': '
        yield ('true' if value else 'false')


def produce_preference_settings_description(user_settings, guild_id):
    """
    Produces preference settings descriptions.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_settings : ``UserSettings``
        The user's settings.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    # preferred_client_id
    preferred_client_id = user_settings.preferred_client_id
    if preferred_client_id:
        preferred_client = CLIENTS.get(preferred_client_id, None)
    else:
        preferred_client = None
    
    yield '- Preferred client: '
    yield (PREFERRED_CLIENT_NAME_DEFAULT if preferred_client is None else preferred_client.name_at(guild_id))
    
    yield '\n- Preferred image source: '
    yield PREFERRED_IMAGE_SOURCE_NAMES.get(user_settings.preferred_image_source, PREFERRED_IMAGE_SOURCE_NAME_DEFAULT)
