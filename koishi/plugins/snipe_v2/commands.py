__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, Emoji, SoundboardSound, Sticker, parse_message_jump_url
from hata.ext.slash import P

from ...bots import FEATURE_CLIENTS

from .caching import update_entity_details
from .component_building import build_add_form, build_view_components
from .permission_helpers import can_add_anywhere
from .responding_helpers import (
    get_attachment_file, get_autocomplete_suggestions_for_emoji_name,
    get_autocomplete_suggestions_for_soundboard_sound_name, get_autocomplete_suggestions_for_sticker_name_or_id,
    get_entity_and_choices_of_emoji_name, get_entity_and_choices_of_message,
    get_entity_and_choices_of_soundboard_sound_name, get_entity_and_choices_of_sticker_name_or_id, pack_feature_flags
)


async def respond_snipe_whole_message(client, interaction_event, message, reveal, detailed):
    """
    Responds on sniping the given message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    message : ``Message``
        The sniped message.
    
    reveal : `bool`
        Whether the message should be revealed for other users as well.
    
    detailed : `bool`
        Whether detailed response should be shown.
    """
    entity, choices = get_entity_and_choices_of_message(message)
    
    if entity is None:
        if interaction_event.is_unanswered():
            function = Client.interaction_response_message_create
        else:
            function = Client.interaction_response_message_edit
        
        await function(
            client,
            interaction_event,
            'The message has nothing to snipe.',
            show_for_invoking_user_only = True,
        )
        return
    
    
    if detailed:
        if interaction_event.is_unanswered():
            await client.interaction_application_command_acknowledge(
                interaction_event,
                False,
                show_for_invoking_user_only = True,
            )
        
        await update_entity_details(entity)
    
    
    feature_flags = pack_feature_flags(interaction_event, detailed, reveal)
    
    components = build_view_components(
        client,
        interaction_event.user,
        feature_flags,
        entity,
        choices,
        interaction_event.guild_id,
    )
    file = get_attachment_file(client, entity)
    
    # Respond
    if not interaction_event.is_unanswered():
        if not reveal:
            await client.interaction_response_message_edit(
                interaction_event,
                allowed_mentions = None,
                components = components,
                file = file,
            )
        else:
            await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
            await client.interaction_response_message_delete(interaction_event)
            await client.interaction_followup_message_create(
                interaction_event,
                allowed_mentions = None,
                components = components,
                file = file,
            )
    
    else:
        if file is None:
            await client.interaction_response_message_create(
                interaction_event,
                allowed_mentions = None,
                components = components,
                show_for_invoking_user_only = (not reveal),
            )
        else:
            await client.interaction_application_command_acknowledge(
                interaction_event,
                show_for_invoking_user_only = (not reveal),
            )
            
            await client.interaction_response_message_edit(
                interaction_event,
                allowed_mentions = None,
                components = components,
                file = file,
            )


@FEATURE_CLIENTS.interactions(
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    target = 'message',
)
async def snipe(client, interaction_event, target):
    """
    Snipes the emojis, reactions and stickers of the message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    target : ``Message``
        the targeted message by the user.
    """
    await respond_snipe_whole_message(client, interaction_event, target, False, False)


SNIPE_COMMANDS = FEATURE_CLIENTS.interactions(
    None,
    integration_types = ['guild_install', 'user_install'],
    is_global = True,
    name = 'snipe',
    description = 'Snipe expressions.',
)


@SNIPE_COMMANDS.interactions(name = 'message')
async def snipe_message_with_url(
    client,
    interaction_event,
    message_jump_url: ('str', 'Message\'s url.'),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Snipes the message defined by its url.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    message_jump_url : `str`
        The message's url to resolve.
    
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    """
    guild_id, channel_id, message_id = parse_message_jump_url(message_jump_url)
    if not message_id:
        await client.interaction_response_message_create(
            interaction_event,
            'The message has nothing to snipe.',
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    try:
        message = await client.message_get((channel_id, message_id))
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code in (
            ERROR_CODES.unknown_channel, # message deleted
            ERROR_CODES.unknown_message, # channel deleted
        ):
            # The message is already deleted.
            error_message = 'The message has been already deleted.'
        
        # Client not in the guild
        elif err.code == ERROR_CODES.missing_access: # client removed
           error_message = 'I am not in the guild.' if guild_id else 'I am not in the channel.'
        
        # No permissions?
        elif err.code == ERROR_CODES.missing_permissions: # no permissions
            error_message = 'I lack permission to get that message.'
        
        else:
            raise
    
    else:
        error_message = None
    
    if (error_message is not None):
        await client.interaction_response_message_edit(
            interaction_event,
            error_message,
        )
        return
    
    await respond_snipe_whole_message(client, interaction_event, message, reveal, detailed)


async def snipe_emoji(
    client,
    interaction_event,
    emoji_name: P(str, 'The emoji, or it\'s name.', 'emoji', min_length = 1, max_length = 100),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Shows details about the selected emoji.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    emoji_name : `str`
        The emoji's name to resolve.
    
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    """
    entity, choices = get_entity_and_choices_of_emoji_name(interaction_event, emoji_name)
    if entity is None:
        await client.interaction_response_message_create(
            interaction_event,
            allowed_mentions = None,
            content = f'Could not resolve any emoji from: {emoji_name[:100]}',
            show_for_invoking_user_only = True,
        )
        return
    
    feature_flags = pack_feature_flags(interaction_event, detailed, reveal)
    
    await client.interaction_response_message_create(
        interaction_event,
        allowed_mentions = None,
        components = build_view_components(
            client,
            interaction_event.user,
            feature_flags,
            entity,
            choices,
            interaction_event.guild_id,
        ),
        show_for_invoking_user_only = (not reveal),
    )


snipe_emoji_plain = SNIPE_COMMANDS.interactions(snipe_emoji, name = 'emoji')
snipe_emoji_autocompleted = SNIPE_COMMANDS.interactions(snipe_emoji, name = 'emoji-autocompleted')
snipe_emoji_autocompleted.autocomplete('emoji', function = get_autocomplete_suggestions_for_emoji_name)


@SNIPE_COMMANDS.interactions(name = 'soundboard-sound')
async def snipe_soundboard_sound(
    client,
    interaction_event,
    soundboard_sound_name: P(
        str,
        'SoundboardSound to show',
        'soundboard-sound',
        min_length = 1,
        max_length = 100,
        autocomplete = get_autocomplete_suggestions_for_soundboard_sound_name,
    ),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Shows details about the selected soundboard sound.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    soundboard_sound_name : `str`
        The soundboard sound's name.
    
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    entity, choices = await get_entity_and_choices_of_soundboard_sound_name(interaction_event, soundboard_sound_name)
    if entity is None:
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            content = f'Could not resolve any soundboard sound from: {soundboard_sound_name!s}',
        )
        return
    
    feature_flags = pack_feature_flags(interaction_event, detailed, reveal)
    
    if not reveal:
        function = Client.interaction_response_message_edit
    
    else:
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        function = Client.interaction_followup_message_create
    
    await function(
        client,
        interaction_event,
        allowed_mentions = None,
        components = build_view_components(
            client,
            interaction_event.user,
            feature_flags,
            entity,
            choices,
            interaction_event.guild_id,
        ),
        file = get_attachment_file(client, entity),
    )


@SNIPE_COMMANDS.interactions(name = 'sticker')
async def snipe_sticker(
    client,
    interaction_event,
    sticker_name_or_id: P(
        str,
        'Sticker to show',
        'sticker',
        min_length = 1,
        max_length = 100,
        autocomplete = get_autocomplete_suggestions_for_sticker_name_or_id,
    ),
    reveal: (bool, 'Should others see it too?') = False,
    detailed: (bool, 'Show detailed view by default?') = False,
):
    """
    Shows details about the selected sticker.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    sticker_name_or_id : `str`
        The sticker's identifier or name to resolve.
    
    reveal : `bool` = `False`, Optional
        Whether the message should be revealed for other users as well.
    
    detailed : `bool` = `False`, Optional
        Whether detailed view should be shown.
    """
    await client.interaction_application_command_acknowledge(
        interaction_event,
        False,
        show_for_invoking_user_only = True,
    )
    
    entity, choices = await get_entity_and_choices_of_sticker_name_or_id(interaction_event, sticker_name_or_id)
    if entity is None:
        await client.interaction_response_message_edit(
            interaction_event,
            allowed_mentions = None,
            content = f'Could not resolve any sticker from: {sticker_name_or_id!s}',
        )
        return
    
    feature_flags = pack_feature_flags(interaction_event, detailed, reveal)
    
    if not reveal:
        function = Client.interaction_response_message_edit
    
    else:
        await client.interaction_response_message_edit(interaction_event, '-# _ _ ')
        await client.interaction_response_message_delete(interaction_event)
        function = Client.interaction_followup_message_create
    
    await function(
        client,
        interaction_event,
        allowed_mentions = None,
        components = build_view_components(
            client,
            interaction_event.user,
            feature_flags,
            entity,
            choices,
            interaction_event.guild_id,
        ),
        file = get_attachment_file(client, entity),
    )


@SNIPE_COMMANDS.interactions(name = 'add')
async def invoke_add(
    client,
    interaction_event,
    type_ : ([('Emoji', 0), ('Sticker', 1), ('Sound', 2)], 'Select what you want to add'),
):
    """
    Shows details about the given emoji.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    type_ : `int`
        The type of entity to be added.
    """
    while True:
        if type_ == 0:
            entity_type = Emoji
        elif type_ == 1:
            entity_type = Sticker
        elif type_ == 2:
            entity_type = SoundboardSound
        else:
            error_message = 'Unknown type selected.'
            break
        
        if not can_add_anywhere(entity_type, None, interaction_event.user):
            error_message = 'We do not share a guild where an emoji could be added to.'
            break
        
        await client.interaction_form_send(
            interaction_event,
            build_add_form(interaction_event.user, entity_type, None, interaction_event.guild_id),
        )
        return
    
    await client.interaction_response_message_create(
        interaction_event,
        content = error_message,
        show_for_invoking_user_only = True,
    )
