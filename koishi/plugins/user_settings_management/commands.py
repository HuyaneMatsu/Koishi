__all__ = ()

from hata import CLIENTS, ClientUserBase, Permission
from hata.ext.slash import P

from ...bot_utils.constants import GUILD__SUPPORT
from ...bots import MAIN_CLIENT

from ..user_settings import (
    FEATURE_SETTINGS_CHOICES, FEATURE_SETTING_RESOLUTION, NOTIFICATION_SETTINGS_CHOICES,
    NOTIFICATION_SETTING_RESOLUTION, OPTION_PREFERRED_CLIENT_ID, OPTION_PREFERRED_IMAGE_SOURCE,
    PREFERRED_IMAGE_SOURCE_NAMES, PREFERRED_IMAGE_SOURCE_NAME_DEFAULT, autocomplete_user_settings_preferred_client,
    build_user_settings_components, get_one_user_settings, get_user_settings_preferred_client, save_one_user_settings
)


COMMAND = MAIN_CLIENT.interactions(
    None,
    description = 'Manage others\' user settings.',
    guild = GUILD__SUPPORT,
    name = 'user-settings-management',
    required_permissions = Permission().update_by_keys(administrator = True),
)


@COMMAND.interactions(name = 'list')
async def command_list(
    client,
    interaction_event,
    user : (ClientUserBase, 'Whom?'),
):
    """
    Lists the user settings of teh selected user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    user : ``ClientUserBase``
        Who's user setting to list.
    """
    if not client.is_owner(interaction_event.user):
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
    )
    user_settings = await get_one_user_settings(user.id)
    await client.interaction_response_message_edit(
        interaction_event,
        components = build_user_settings_components(user_settings, interaction_event.guild_id),
    )



@COMMAND.interactions(name = 'feature-settings-change')
async def feature_settings_change(
    client,
    interaction_event,
    user : (ClientUserBase, 'Whom?'),
    feature_type: (FEATURE_SETTINGS_CHOICES, 'Select the feature to change.'),
    enabled: (bool, 'Whether the feature should be enabled.'),
):
    """
    SetS feature setting.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    user : ``ClientUserBase``
        Who's user setting to modify.
    
    feature_type : `int`
        The feature's type.
    
    enabled : `bool`
        Whether we should enable the feature.
    """
    if not client.is_owner(interaction_event.user):
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
    )
    user_settings = await get_one_user_settings(user.id)
    
    option = FEATURE_SETTING_RESOLUTION[feature_type]
    previous = option.get(user_settings)
    option.set(user_settings, enabled)
    
    await save_one_user_settings(user_settings)
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = f'{option.display_name} : {"true" if previous else "false"} -> {"true" if enabled else "false"}',
    )


@COMMAND.interactions(name = 'notification-settings-change')
async def notification_settings_change(
    client,
    interaction_event,
    user : (ClientUserBase, 'Whom?'),
    notification_type: (NOTIFICATION_SETTINGS_CHOICES, 'Select the notification to change.'),
    enabled: (bool, 'Whether the notification should be enabled.'),
):
    """
    Sets notification setting.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    user : ``ClientUserBase``
        Who's user setting to modify.
    
    notification_type : `int`
        The notification's type.
    
    enabled : `bool`
        Whether we should enable the notification.
    """
    if not client.is_owner(interaction_event.user):
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
    )
    user_settings = await get_one_user_settings(user.id)
    
    option = NOTIFICATION_SETTING_RESOLUTION[notification_type]
    previous = option.get(user_settings)
    option.set(user_settings, enabled)
    
    await save_one_user_settings(user_settings)
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = f'{option.display_name} : {"true" if previous else "false"} -> {"true" if enabled else "false"}',
    )


@COMMAND.interactions(name = 'preferred-client-set')
async def preferred_client_set(
    client,
    interaction_event,
    user : (ClientUserBase, 'Whom?'),
    client_name : P(str, 'Select a client', 'client', autocomplete = autocomplete_user_settings_preferred_client),
):
    """
    Sets preferred client.
    
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
    if not client.is_owner(interaction_event.user):
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
    )
    user_settings = await get_one_user_settings(user.id)
    
    hit, chosen_client = get_user_settings_preferred_client(interaction_event, client_name)
    if not hit:
        await client.interaction_response_message_edit(
            interaction_event,
            content = 'Could not identify client.',
        )
        return
    
    previous = OPTION_PREFERRED_CLIENT_ID.get(user_settings)
    previous_client = CLIENTS.get(previous, None)
    OPTION_PREFERRED_CLIENT_ID.set(user_settings, 0 if chosen_client is None else chosen_client.id)
    
    await save_one_user_settings(user_settings)
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = (
            f'{OPTION_PREFERRED_CLIENT_ID.display_name} : '
            f'{"null" if previous_client is None else previous_client.name_at(interaction_event.guild_id)} -> '
            f'{"null" if chosen_client is None else chosen_client.name_at(interaction_event.guild_id)}'
        ),
    )


@COMMAND.interactions(name = 'preferred-image-source-set')
async def preferred_image_source_set(
    client,
    interaction_event,
    user : (ClientUserBase, 'Whom?'),
    value : (
        [(value, key) for key, value in sorted(PREFERRED_IMAGE_SOURCE_NAMES.items())],
        'Select an image source',
        'source',
    ),
):
    """
    Sets preferred image source.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    
    interaction_event : ``InteractionEvent``
        The received event.
    
    value : `int`
        Image source identifier.
    """
    if not client.is_owner(interaction_event.user):
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
    )
    user_settings = await get_one_user_settings(user.id)
    
    if value not in PREFERRED_IMAGE_SOURCE_NAMES.keys():
        await client.interaction_response_message_edit(
            interaction_event,
            content = 'Could not identify image source.',
        )
        return
    
    previous = OPTION_PREFERRED_IMAGE_SOURCE.get(user_settings)
    OPTION_PREFERRED_IMAGE_SOURCE.set(user_settings, value)
    
    await save_one_user_settings(user_settings)
    
    await client.interaction_response_message_edit(
        interaction_event,
        content = (
            f'{OPTION_PREFERRED_IMAGE_SOURCE.display_name} : '
            f'{PREFERRED_IMAGE_SOURCE_NAMES.get(previous, PREFERRED_IMAGE_SOURCE_NAME_DEFAULT)} -> '
            f'{PREFERRED_IMAGE_SOURCE_NAMES.get(value, PREFERRED_IMAGE_SOURCE_NAME_DEFAULT)}'
        ),
    )
