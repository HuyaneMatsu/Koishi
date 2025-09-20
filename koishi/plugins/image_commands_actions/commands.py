__all__ = ()

from hata import DiscordException, ERROR_CODES
from hata.ext.slash import P, abort

from ...bots import FEATURE_CLIENTS

from ..user_settings import get_one_user_settings, get_preferred_client_in_channel

from .action import (
    COOLDOWN_HANDLER, build_response, create_action_command_function, create_response_embed, get_allowed_users,
    send_action_response, send_action_response_to
)
from .action_filtering import (
    PARAMETER_NAME_ACTION_TAG, PARAMETER_NAME_NAME, PARAMETER_NAME_SOURCE, PARAMETER_NAME_TARGET,
    get_action_tag_suggestions, get_name_suggestions, get_source_character_suggestions,
    get_target_character_suggestions, get_action_and_image_detail
)
from .actions import ACTIONS
from .events import PERMISSION_IMAGES


# Register action commands.

for action in ACTIONS:
    
    FEATURE_CLIENTS.interactions(
        create_action_command_function(action),
        description = action.description,
        integration_types = ['guild_install', 'user_install'],
        is_global = True,
        name = action.name,
    )

# cleanup
del action


async def get_should_use_default_response_method(client, event):
    """
    Returns whether we should use the default response method and the client to execute the responding with.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    should_use_default_response_method : `bool`
    client : ``Client``
    """
    if event.user_permissions.use_external_application_commands:
        return True, client
    
    guild = event.guild
    if (guild is None) or (client not in guild.clients):
        return True, client
    
    # Select client based on user settings if available.
    user_settings = await get_one_user_settings(event.user.id)
    preferred_client = get_preferred_client_in_channel(
        event.channel, user_settings.preferred_client_id, client, PERMISSION_IMAGES
    )
    return False, preferred_client


@FEATURE_CLIENTS.interactions(
    name = 'action',
    description = 'Reality is subjective and all is mental.',
    is_global = True,
    integration_types = ['guild_install', 'user_install'],
)
async def wild_card_action(
    client,
    event,
    action_tag_name : P(str, 'Select action tag', PARAMETER_NAME_ACTION_TAG) = None,
    source_character_name : P(str, 'Source character name.', PARAMETER_NAME_SOURCE) = None,
    target_character_name : P(str, 'Target character mame.', PARAMETER_NAME_TARGET) = None,
    image_name : P(str, 'Image name', PARAMETER_NAME_NAME) = None,
    target_00: ('mentionable', 'Select someone', 'target-1') = None,
    target_01: ('mentionable', 'Select someone', 'target-2') = None,
    target_02: ('mentionable', 'Select someone', 'target-3') = None,
    target_03: ('mentionable', 'Select someone', 'target-4') = None,
    target_04: ('mentionable', 'Select someone', 'target-5') = None,
    target_05: ('mentionable', 'Select someone', 'target-6') = None,
    target_06: ('mentionable', 'Select someone', 'target-7') = None,
    target_07: ('mentionable', 'Select someone', 'target-8') = None,
    target_08: ('mentionable', 'Select someone', 'target-9') = None,
    target_09: ('mentionable', 'Select someone', 'target-10') = None,
):
    """
    Wild card action call.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    action_tag_name : `None | str` = `None`, Optional
        Selected action tag name.
    source_character_name : `None | str` = `None`, Optional
        Name of the source character.
    target_character_name : `None | str` = `None`, Optional
        Name of the target character.
    image_name : `None | str` = `None`, Optional
        The name of the image.
    user_{n} : ``None | ClientUserBase`` = `None`, Optional
        Additional users to target.
    """
    targets, client_in_users, user_in_users, allowed_mentions = get_allowed_users(
        client,
        event,
        (
            target_00, target_01, target_02, target_03, target_04, target_05, target_06, target_07, target_08,
            target_09,
        ),
    )
    
    expire_after = COOLDOWN_HANDLER.get_cooldown(event, len(targets))
    if expire_after > 0.0:
        abort(
            f'{client.name_at(event.guild_id)} got bored of enacting your {event.name} try again in '
            f'{expire_after:.2f} seconds.'
        )
    action, image_detail = get_action_and_image_detail(
        action_tag_name, source_character_name, target_character_name, image_name
    )
    if (action is None):
        abort('Could not match any actions.')
    
    if (image_detail is None):
        abort('Could not match any images.')
    
    # Reverse the users when there are no target.
    if (not targets) and (not client_in_users):
        source_user = client
        targets = {event.user}
    else:
        source_user = event.user
    
    content = build_response(client, action.starter_text, action.verb, source_user, targets, client_in_users)
    embed = create_response_embed(client, event.guild_id, event.user, targets, client_in_users, image_detail)
    
    
    should_use_default_response_method, client = await get_should_use_default_response_method(client, event)
    if should_use_default_response_method:
        await send_action_response(client, event, content, embed, allowed_mentions)
        return
    
    try:
        await client.interaction_response_message_create(
            event, 'Reality is subjective and all is mental.', show_for_invoking_user_only = True
        )
    except ConnectionError:
        return
    
    except DiscordException as exception:
        if exception.status >= 500:
            return
        
        if exception.code != ERROR_CODES.unknown_interaction:
            raise
    
    await send_action_response_to(client, event.channel, content, embed, allowed_mentions)
    return


@wild_card_action.autocomplete('action_tag_name')
async def autocomplete_action_tag_name(client, interaction_event, value):
    """
    Autocompletes the tag name field.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value typed by the user.
    """
    try:
        await client.interaction_application_command_autocomplete(
            interaction_event,
            get_action_tag_suggestions(interaction_event, value),
        )
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            (exception.status < 500) and
            (exception.code != ERROR_CODES.unknown_interaction)
        ):
            raise


@wild_card_action.autocomplete('source_character_name')
async def autocomplete_source_character_name(client, interaction_event, value):
    """
    Autocompletes the source character name field.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value typed by the user.
    """
    try:
        await client.interaction_application_command_autocomplete(
            interaction_event,
            get_source_character_suggestions(interaction_event, value),
        )
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            (exception.status < 500) and
            (exception.code != ERROR_CODES.unknown_interaction)
        ):
            raise


@wild_card_action.autocomplete('target_character_name')
async def autocomplete_target_character_name(client, interaction_event, value):
    """
    Autocompletes the target character name field.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value typed by the user.
    """
    try:
        await client.interaction_application_command_autocomplete(
            interaction_event,
            get_target_character_suggestions(interaction_event, value),
        )
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            (exception.status < 500) and
            (exception.code != ERROR_CODES.unknown_interaction)
        ):
            raise


@wild_card_action.autocomplete('image_name')
async def autocomplete_image_name(client, interaction_event, value):
    """
    Autocompletes the image name field.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received this interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value typed by the user.
    """
    try:
        await client.interaction_application_command_autocomplete(
            interaction_event,
            get_name_suggestions(interaction_event, value),
        )
    except ConnectionError:
        pass
    
    except DiscordException as exception:
        if (
            (exception.status < 500) and
            (exception.code != ERROR_CODES.unknown_interaction)
        ):
            raise
