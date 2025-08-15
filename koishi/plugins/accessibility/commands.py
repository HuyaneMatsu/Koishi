__all__ = ()

from hata.ext.slash import P

from ...bots import FEATURE_CLIENTS

from ..user_settings import (
    NOTIFICATION_SETTINGS_CHOICES, NOTIFICATION_SETTING_RESOLUTION, PREFERRED_IMAGE_SOURCE_NAMES,
    autocomplete_user_settings_preferred_client, build_notification_settings_embed, build_preference_settings_embed,
    get_one_user_settings, handle_user_settings_change, handle_user_settings_set_preferred_client,
    handle_user_settings_set_preferred_image_source
)
from ..touhou_character_preference import (
    PREFERRED_CHARACTER_MAX, add_touhou_character_to_preference, build_character_preference_change_embed,
    build_character_preference_embed, get_one_touhou_character_preference, remove_touhou_character_from_preference
)
from ..touhou_core import (
    auto_complete_touhou_character_name, get_touhou_character_like, get_touhou_character_names_like_from
)


ACCESSIBILITY_INTERACTIONS = FEATURE_CLIENTS.interactions(
    None,
    name = 'accessibility',
    description = 'Customize your Koishi experience. (Actually just a few things.)',
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
)

NOTIFICATION_SETTINGS = ACCESSIBILITY_INTERACTIONS.interactions(
    None,
    name = 'notification-settings',
    description = 'Customize your notification settings. (Really just a few things.)'
)


@NOTIFICATION_SETTINGS.interactions(name = 'show')
async def notification_settings_show(client, interaction_event):
    """
    Shows your notification settings.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user_settings = await get_one_user_settings(interaction_event.user_id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        embed = build_notification_settings_embed(interaction_event.user, user_settings),
    )


@NOTIFICATION_SETTINGS.interactions(name = 'change')
async def notification_settings_change(
    client,
    interaction_event,
    notification_type: (NOTIFICATION_SETTINGS_CHOICES, 'Select the notification to change.'),
    enabled: (bool, 'Whether the notification should be enabled.'),
):
    """
    Set your notification setting.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    notification_type : `int`
        The notification's type.
    
    enabled : `bool`
        Whether we should enable the notification.
    
    """
    await handle_user_settings_change(
        client, interaction_event, NOTIFICATION_SETTING_RESOLUTION[notification_type], enabled
    )


PREFERENCE_SETTINGS = ACCESSIBILITY_INTERACTIONS.interactions(
    None,
    name = 'preference-settings',
    description = 'Customize your preference settings. (Really just a few things.)'
)

@PREFERENCE_SETTINGS.interactions(name = 'show')
async def preference_settings_show(client, interaction_event):
    """
    Shows your preference settings.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user_settings = await get_one_user_settings(interaction_event.user_id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        embed = build_preference_settings_embed(interaction_event.user, user_settings),
    )


@PREFERENCE_SETTINGS.interactions(name = 'set-preferred-client')
async def preference_settings_set_preferred_client(
    client,
    interaction_event,
    client_name : P(str, 'Select a client', 'client', autocomplete = autocomplete_user_settings_preferred_client),
):
    """
    Set which client you would like to get / send messages with if option is available.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    client_name : `str`
        The client's name.
    """
    await handle_user_settings_set_preferred_client(client, interaction_event, client_name)


@PREFERENCE_SETTINGS.interactions(name = 'set-preferred-image-source')
async def preference_settings_set_preferred_image_source(
    client,
    interaction_event,
    value : (
        [(value, key) for key, value in sorted(PREFERRED_IMAGE_SOURCE_NAMES.items())],
        'Select an image source',
        'source',
    ),
):
    """
    Set which image source you would like to pool images from if option is available.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    client_name : `str`
        The client's name.
    """
    await handle_user_settings_set_preferred_image_source(client, interaction_event, value)


CHARACTER_PREFERENCE = ACCESSIBILITY_INTERACTIONS.interactions(
    None,
    name = 'character-preference',
    description = 'Customize your character preference. (Really just a few things.)'
)


@CHARACTER_PREFERENCE.interactions(name = 'show')
async def character_preference_show(client, interaction_event):
    """
    Shows your preferred character(s).
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    """
    user = interaction_event.user
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    character_preferences = await get_one_touhou_character_preference(user.id)
    
    await client.interaction_response_message_edit(
        interaction_event,
        embed = build_character_preference_embed(user, character_preferences),
    )


@CHARACTER_PREFERENCE.interactions(name = 'add')
async def character_preference_add(
    client,
    interaction_event,
    name : P(str, 'Select a character', autocomplete = auto_complete_touhou_character_name),
):
    """
    Shows your preferred character(s).
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    name : `str`
        Character's name.
    """
    character = get_touhou_character_like(name)
    if (character is None):
        await client.interaction_response_message_create(
            interaction_event,
            'Could not identify character.',
            show_for_invoking_user_only = True,
        )
        return
    
    user = interaction_event.user
    character_preferences = await get_one_touhou_character_preference(user.id)
    if (character_preferences is not None) and (len(character_preferences) >= PREFERRED_CHARACTER_MAX):
        await client.interaction_response_message_create(
            interaction_event,
            f'Can not add more character preferences. ({len(character_preferences)!r} / {PREFERRED_CHARACTER_MAX!r})',
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    await add_touhou_character_to_preference(user.id, character)
    
    await client.interaction_response_message_edit(
        interaction_event,
        embed = build_character_preference_change_embed(user, character, True),
    )


@CHARACTER_PREFERENCE.interactions(name = 'remove')
async def character_preference_remove(
    client,
    interaction_event,
    name : (str, 'Select a character'),
):
    """
    Shows your preferred character(s).
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    name : `str`
        Character's name.
    """
    character = get_touhou_character_like(name)
    if (character is None):
        await client.interaction_response_message_create(
            interaction_event,
            'Could not identify character.',
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
    )
    
    user = interaction_event.user
    await remove_touhou_character_from_preference(user.id, character)
    
    await client.interaction_followup_message_edit(
        interaction_event,
        embed = build_character_preference_change_embed(user, character, False),
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
