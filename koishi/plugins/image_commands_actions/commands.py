__all__ = ()

from hata import DiscordException, ERROR_CODES
from hata.ext.slash import P, abort

from ...bots import FEATURE_CLIENTS

from .action import (
    COOLDOWN_HANDLER, build_response, can_send_response_to_channel, create_action_command_function,
    create_response_embed, get_allowed_users, send_action_response_to
)
from .action_filtering import (
    PARAMETER_NAME_ACTION_TAG, PARAMETER_NAME_NAME, PARAMETER_NAME_SOURCE, PARAMETER_NAME_TARGET,
    autocomplete_action_tag, autocomplete_name, autocomplete_source, autocomplete_target, get_action_and_image_detail
)
from .actions import ACTIONS


# Register action commands.

for action in ACTIONS:
    
    FEATURE_CLIENTS.interactions(
        create_action_command_function(action),
        name = action.name,
        description = action.description,
        is_global = True,
        integration_types = (
            ['guild_install', 'user_install']
            if action.handler.is_character_filterable() else
            ['guild_install']
        ),
    )

# cleanup
del action


@FEATURE_CLIENTS.interactions(
    name = 'action',
    description = 'Reality is subjective and all is mental.',
    is_global = True,
    integration_types = ['user_install'],
)
async def wild_card_action(
    client,
    event,
    action_tag_name : P(str, 'Select action tag', PARAMETER_NAME_ACTION_TAG, autocomplete = autocomplete_action_tag) = None,
    source_character_name : P(str, 'Source character name.', PARAMETER_NAME_SOURCE, autocomplete = autocomplete_source) = None,
    target_character_name : P(str, 'Target character mame.', PARAMETER_NAME_TARGET, autocomplete = autocomplete_target) = None,
    image_name : P(str, 'Image name', PARAMETER_NAME_NAME, autocomplete = autocomplete_name) = None,
    target_00: ('mentionable', 'Select someone.', 'target-1') = None,
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
    user_{n} : `None`, ``ClientUserBase`` = `None`, Optional
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
            f'{client.name_at(event.guild_id)} got bored of enacting your {event.interaction.name} try again in '
            f'{expire_after:.2f} seconds.'
        )
    
    action, image_detail = get_action_and_image_detail(
        action_tag_name, source_character_name, target_character_name, image_name
    )
    if (action is None):
        abort('Could not match any actions.')
    
    if (image_detail is None):
        abort('Could not match any images.')
    
    content = build_response(client, action.verb, event.user, targets, client_in_users)
    embed = create_response_embed(client, event.guild_id, event.user, targets, client_in_users, image_detail)
    
    guild = event.guild
    if (guild is None) or (client not in guild.clients) or (not can_send_response_to_channel(client, event.channel)):
        await send_action_response_to(client, event.channel, content, embed, allowed_mentions)
        return
    
    try:
        await client.interaction_response_message_create(
            event, 'Reality is subjective and all is mental.', show_for_invoking_user_only = True
        )
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code != ERROR_CODES.unknown_interaction:
            raise
    
    await send_action_response_to(client, event.channel, content, embed, allowed_mentions)
