__all__ = ()

from hata.ext.slash import InteractionResponse, P, abort

from ...bots import SLASH_CLIENT

from ..notification_settings import (
    NOTIFICATION_SETTINGS_CHOICES, NOTIFICATION_SETTING_RESOLUTION, build_notification_settings_embed,
    get_one_notification_settings, handle_notification_settings_change
)
from ..touhou_character_preference import (
    PREFERRED_CHARACTER_MAX, add_touhou_character_to_preference, build_character_preference_change_embed,
    build_character_preference_embed, get_one_touhou_character_preference, remove_touhou_character_from_preference
)
from ..touhou_core import (
    auto_complete_touhou_character_name, get_touhou_character_like, get_touhou_character_names_like_from
)


ACCESSIBILITY_INTERACTIONS = SLASH_CLIENT.interactions(
    None,
    name = 'accessibility',
    description = 'Customize your Koishi experience. (Actually just a few things.)',
    is_global = True,
)

NOTIFICATION_SETTINGS = ACCESSIBILITY_INTERACTIONS.interactions(
    None,
    name = 'notification-settings',
    description = 'Customize your notification settings. (Really just a few things.)'
)


@NOTIFICATION_SETTINGS.interactions(name = 'show')
async def notification_settings_show(event):
    """
    Shows your notification settings.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    user = event.user
    notification_settings = await get_one_notification_settings(user.id)
    return InteractionResponse(
        embed = build_notification_settings_embed(user, notification_settings),
        show_for_invoking_user_only = True,
    )


@NOTIFICATION_SETTINGS.interactions(name = 'change')
async def notification_settings_change(
    event,
    notification_type: (NOTIFICATION_SETTINGS_CHOICES, 'Select the notification to change.'),
    enabled: (bool, 'Whether the notification should be enabled.'),
):
    """
    Set your notification setting.
    
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    notification_type : `int`
        The notification's type.
    enabled : `bool`
        Whether we should enable the notification.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    return await handle_notification_settings_change(
        event, NOTIFICATION_SETTING_RESOLUTION[notification_type], enabled
    )


CHARACTER_PREFERENCE = ACCESSIBILITY_INTERACTIONS.interactions(
    None,
    name = 'character-preference',
    description = 'Customize your character preference. (Really just a few things.)'
)


@CHARACTER_PREFERENCE.interactions(name = 'show')
async def character_preference_show(event):
    """
    Shows your preferred character(s).
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    user = event.user
    character_preferences = await get_one_touhou_character_preference(user.id)
    return InteractionResponse(
        embed = build_character_preference_embed(user, character_preferences),
        show_for_invoking_user_only = True,
    )


@CHARACTER_PREFERENCE.interactions(name = 'add')
async def character_preference_add(
    event,
    name : P(str, 'Select a character', autocomplete = auto_complete_touhou_character_name),
):
    """
    Shows your preferred character(s).
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    name : `str`
        Character's name.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    character = get_touhou_character_like(name)
    if (character is None):
        abort('Could not identify character.')
    
    user = event.user
    character_preferences = await get_one_touhou_character_preference(user.id)
    if (character_preferences is not None) and (len(character_preferences) >= PREFERRED_CHARACTER_MAX):
        abort(f'Can not add more character preferences. ({len(character_preferences)!r} / {PREFERRED_CHARACTER_MAX!r})')
    
    await add_touhou_character_to_preference(user.id, character)
    
    return InteractionResponse(
        embed = build_character_preference_change_embed(user, character, True),
        show_for_invoking_user_only = True,
    )


@CHARACTER_PREFERENCE.interactions(name = 'remove')
async def character_preference_remove(
    event,
    name : (str, 'Select a character'),
):
    """
    Shows your preferred character(s).
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event.
    name : `str`
        Character's name.
    
    Returns
    -------
    response : ``InteractionResponse``
    """
    character = get_touhou_character_like(name)
    if (character is None):
        abort('Could not identify character.')
    
    user = event.user
    await remove_touhou_character_from_preference(user.id, character)
    
    return InteractionResponse(
        embed = build_character_preference_change_embed(user, character, False),
        show_for_invoking_user_only = True,
    )


@character_preference_remove.autocomplete('name')
async def autocomplete_character_preference_name(event, name):
    """
    Auto completes touhou character name from the options of the user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received event
    name : `None`, `str`
        Input of the user.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    user = event.user
    character_preferences = await get_one_touhou_character_preference(user.id)
    if character_preferences is None:
        return None
    
    # Collect characters
    characters = None
    
    for character_preference in character_preferences:
        character = character_preference.get_character()
        if (character is not None):
            if characters is None:
                characters = []
            
            characters.append(character)
    
    if characters is None:
        return None
    
    # No name -> list all characters
    if name is None:
        return [character.name for character in characters]
    
    # Yes name -> get matches
    return get_touhou_character_names_like_from(name, characters)
