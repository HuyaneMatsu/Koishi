__all__ = ()

from hata import Client, DiscordException, ERROR_CODES, Emoji, GUILDS, InteractionType, SoundboardSound, Sticker

from ...bots import FEATURE_CLIENTS

from .caching import update_entity_details
from .component_building import build_add_form, build_edit_form, build_remove_form, build_view_components
from .constants import (
    ACTION_ADD, ACTION_CLOSE, ACTION_DETAILS, ACTION_DM, ACTION_EDIT, ACTION_REMOVE, ACTION_REVEAL,
    FEATURE_FLAG_DETAILED, FEATURE_FLAG_DM, FEATURE_FLAG_REVEALED, PERMISSION_MASK_EXPRESSION_ADD,
    PERMISSION_MASK_EXPRESSION_EDIT_OR_DELETE
)
from .content_building import get_entity_type_name
from .custom_ids import (
    CUSTOM_ID_ENTITY_DESCRIPTION, CUSTOM_ID_ENTITY_EMOJI, CUSTOM_ID_ENTITY_FILE, CUSTOM_ID_ENTITY_GUILD,
    CUSTOM_ID_ENTITY_NAME, CUSTOM_ID_ENTITY_REASON, CUSTOM_ID_ENTITY_ROLES, CUSTOM_ID_ENTITY_TAGS,
    CUSTOM_ID_ENTITY_VOLUME, CUSTOM_ID_SNIPE_ACTION_PATTERN, CUSTOM_ID_SNIPE_ADD_PATTERN,
    CUSTOM_ID_SNIPE_CHOICE_PATTERN, CUSTOM_ID_SNIPE_EDIT_PATTERN, CUSTOM_ID_SNIPE_REMOVE_PATTERN
)
from .entity_packing import unpack_entity, unpack_entity_type
from .permission_helpers import get_first_client_with_permissions, has_free_entity_spot, has_user_required_permissions
from .responding_helpers import (
    get_attachment_file, identify_input_emoji, identify_input_role_ids, identify_input_tags, parse_choices
)


async def respond_snipe_whole_message(client, interaction_event, feature_flags, entity, choices):
    """
    Responds with a whole message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    feature_flags : `int`
        How the message should be displayed as.
    
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to display.
    
    choices : ``None | list<Emoji | Sticker | SoundboardSound>``
        Additional choices to display.
    """
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if feature_flags & FEATURE_FLAG_DETAILED:
        await update_entity_details(entity)
    
    await client.interaction_response_message_edit(
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


async def respond_snipe_direct_message(client, interaction_event, feature_flags, entity, choices):
    """
    Responds with a direct message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    feature_flags : `int`
        How the message should be displayed as.
    
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to display.
    
    choices : ``None | list<Emoji | Sticker | SoundboardSound>``
        Additional choices to display.
    """
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    channel = await client.channel_private_create(interaction_event.user)
    try:
        await client.message_create(
            channel,
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
    except ConnectionError:
        return
    
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user: # user has dm-s disabled:
            await client.interaction_followup_message_create(
                interaction_event,
                'Could not deliver direct message.',
                show_for_invoking_user_only = True
            )
        
        else:
            raise



async def respond_snipe_whole_message_revealed(client, interaction_event, feature_flags, entity, choices):
    """
    Responds with a revealed message.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        Client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    feature_flags : `int`
        How the message should be displayed as.
    
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to display.
    
    choices : ``None | list<Emoji | Sticker | SoundboardSound>``
        Additional choices to display.
    """
    await client.interaction_component_acknowledge(
        interaction_event,
        False,
    )
    
    if feature_flags & FEATURE_FLAG_DETAILED:
        await update_entity_details(entity)
    
    await client.interaction_followup_message_create(
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
    await client.interaction_response_message_delete(
        interaction_event,
    )


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_CHOICE_PATTERN)
async def handle_snipe_choice(client, interaction_event, user_id, feature_flags, *, selected):
    """
    Handles a snipe choice.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as hexadecimal integer.
    
    feature_flags : `str`
        The current feature flags of the snipe as hexadecimal string.
    
    selected : `None | tuple<str>`, (Keyword only)
        The selected entity.
    """
    try:
        user_id = int(user_id, 16)
        feature_flags = int(feature_flags, 16)
    except ValueError:
        return
    
    if (interaction_event.user_id != user_id):
        return
    
    if (selected is None):
        return
    
    entity = unpack_entity(selected[0])
    if entity is None:
        return
    
    choices = parse_choices(interaction_event, user_id, feature_flags)
    
    await respond_snipe_whole_message(client, interaction_event, feature_flags, entity, choices)


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_ACTION_PATTERN)
async def handle_snipe_action(client, interaction_event, user_id, feature_flags, current_entity_packed, *, selected):
    """
    handles a snipe choice.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the interaction event.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `str`
        The original invoking user's identifier as hexadecimal integer.
    
    feature_flags : `str`
        The current feature flags of the snipe as hexadecimal string.
    
    current_entity_packed : `str`
        The current entity packed.
    
    selected : `None | tuple<str>`, (Keyword only)
        The selected action.
    """
    try:
        user_id = int(user_id, 16)
        feature_flags = int(feature_flags, 16)
    except ValueError:
        return
    
    if (interaction_event.user_id != user_id):
        return
    
    entity = unpack_entity(current_entity_packed)
    if (entity is None):
        return
    
    if (selected is None):
        return
    
    action = selected[0]
    
    choices = parse_choices(interaction_event, user_id, feature_flags)
    
    if action == ACTION_DETAILS:
        feature_flags |= FEATURE_FLAG_DETAILED
        await respond_snipe_whole_message(client, interaction_event, feature_flags, entity, choices)
        return
    
    if action == ACTION_DM:
        feature_flags |= FEATURE_FLAG_DM | FEATURE_FLAG_REVEALED
        await respond_snipe_direct_message(client, interaction_event, feature_flags, entity, choices)
        return
    
    if action == ACTION_REVEAL:
        feature_flags |= FEATURE_FLAG_REVEALED
        await respond_snipe_whole_message_revealed(client, interaction_event, feature_flags, entity, choices)
        return
    
    if action == ACTION_ADD:
        await client.interaction_form_send(
            interaction_event,
            build_add_form(interaction_event.user, type(entity), entity, interaction_event.guild_id),
        )
        return
    
    if action == ACTION_EDIT:
        await client.interaction_form_send(
            interaction_event,
            build_edit_form(entity, interaction_event.guild_id),
        )
        return
    
    if action == ACTION_REMOVE:
        await client.interaction_form_send(
            interaction_event,
            build_remove_form(entity),
        )
        return
    
    if action == ACTION_CLOSE:
        await client.interaction_response_message_delete(
            interaction_event,
        )
        return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_ADD_PATTERN, target = 'form')
async def handle_snipe_add(
    client,
    interaction_event,
    current_entity_packed,
    *,
    guild_ids : CUSTOM_ID_ENTITY_GUILD = None,
    name : CUSTOM_ID_ENTITY_NAME = None,
    roles : CUSTOM_ID_ENTITY_ROLES = None,
    tags : CUSTOM_ID_ENTITY_TAGS = None,
    description : CUSTOM_ID_ENTITY_DESCRIPTION = None,
    emoji : CUSTOM_ID_ENTITY_EMOJI = None,
    volume : CUSTOM_ID_ENTITY_VOLUME = None,
    attachments : CUSTOM_ID_ENTITY_FILE = None,
    reason : CUSTOM_ID_ENTITY_REASON = None,
):
    """
    Handles a snipe add interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    current_entity_packed : `str`
        The packed entity or entity type.
    
    guild_ids : `None | tuple<str>` = `None`, (Keyword only)
        The targeted guilds' identifiers as hexadecimal strings.
    
    name : `None | str` = `None`, Optional (Keyword only)
        Inputted name.
    
    roles : ``None | tuple<Role>`` = `None`, Optional (Keyword only)
        Selected roles.
    
    tags : `None | str` = `None`, Optional (Keyword only)
        Inputted tags.
    
    description : `None | str` = `None`, Optional (Keyword only)
        Input description.
    
    emoji : `None | str` = `None`, Optional (Keyword only)
        Input emoji.
    
    volume : `None | str` = `None`, Optional (Keyword only)
        Input volume.
    
    attachments : ``None | tuple<Attachment>`` = `None`, Optional (Keyword only)
        Input attachment. 
    
    reason : `None | str` = `None`, Optional (Keyword only)
        Input reason.
    """
    if interaction_event.type is InteractionType.application_command:
        await client.interaction_application_command_acknowledge(
            interaction_event,
            False,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_component_acknowledge(
            interaction_event,
            False,
        )
    
    while True:
        # entity & entity_type
        entity = unpack_entity(current_entity_packed)
        if (entity is not None):
            entity_type = type(entity)
        
        else:
            entity_type = unpack_entity_type(current_entity_packed)
            if entity_type is None:
                error_message = 'Could not recognize the entity type to be added.'
                break
        
        # guild
        if (guild_ids is None):
            error_message = 'No guild was selected.'
            break
        
        try:
            guild_id = int(guild_ids[0], 16)
        except ValueError:
            error_message = 'Could not recognize selected guild.'
            break
        
        if not guild_id:
            error_message = 'No guild was selected.'
            break
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            error_message = 'Unknown guild was selected.'
            break
        
        
        if not has_user_required_permissions(guild, interaction_event.user, PERMISSION_MASK_EXPRESSION_ADD):
            error_message = 'You do not have the required permissions.'
            break
        
        executor_client = get_first_client_with_permissions(guild, PERMISSION_MASK_EXPRESSION_ADD)
        if (executor_client is None):
            error_message = 'I do not have the required permissions.'
            break
        
        if not has_free_entity_spot(entity_type, entity, guild):
            error_message = 'The guild has no free spots to add to.'
            break
        
        # Start building the fields.
        fields = {}
        
        # name
        if (name is None):
            error_message = 'Name is required.'
            break
            
        fields['name'] = name
        
        # roles
        if (entity_type is Emoji):
            identified, role_ids_processed = identify_input_role_ids(roles)
            if not identified:
                error_message = 'Could not recognize the inputted roles.'
                break
            
            fields['role_ids'] = role_ids_processed
        
        # tags
        if (entity_type is Sticker):
            identified, tags_processed = identify_input_tags(tags)
            if not identified:
                error_message = 'Could not recognize the inputted tags.'
                break
            
            if (tags_processed is None):
                error_message = 'At least one non-empty tag is required'
                break
            
            fields['tags'] = tags_processed
        
        # description
        if (entity_type is Sticker):
            fields['description'] = description
        
        # emoji
        if (entity_type is SoundboardSound):
            identified, emoji_processed = identify_input_emoji(guild, emoji)
            if not identified:
                error_message = 'Could not recognize the inputted emoji.'
                break
            
            if (
                (emoji_processed is not None) and
                emoji_processed.is_custom_emoji() and
                (emoji_processed.guild_id != guild_id)
            ):
                error_message = 'Emoji of other guilds are not available to be chosen.'
                break
            
            fields['emoji'] = emoji_processed
        
        # volume
        if (entity_type is SoundboardSound):
            if volume is None:
                volume = 1.0
            else:
                try:
                    volume = float(volume)
                except ValueError:
                    error_message = 'Invalid volume format.'
                    break
                
                if volume <= 0.0:
                    error_message = 'Volume must be greater than 0.0.'
                    break
                
                if volume > 1.0:
                    error_message = 'Volume must be lower or equal to 1.0.'
                    break
            
            fields['volume'] = volume
        
        if (attachments is not None):
            if entity_type is Emoji:
                entity_max_size = 262144
            elif entity_type is Sticker:
                entity_max_size = 524288
            elif entity_type is SoundboardSound:
                entity_max_size = 1048576
            else:
                entity_max_size = 1048576
            
            attachment = attachments[0]
            if attachment.size > entity_max_size:
                error_message = f'Attachment size over allowed limit; {attachment.size!s} > {entity_max_size!s}.'
                break
            
            data = await client.download_attachment(attachment)
        
        elif (entity is not None):
            async with client.http.get(entity.url) as response:
                data = await response.read()
        
        else:
            error_message = 'Please provide a file.'
            break
        
        try:
            if entity_type is Emoji:
                await executor_client.emoji_create_guild(
                    guild,
                    image = data,
                    reason = reason,
                    **fields,
                )
            
            elif entity_type is Sticker:
                await executor_client.sticker_create(
                    guild,
                    image = data,
                    reason = reason,
                    **fields,
                )
            
            elif entity_type is SoundboardSound:
                await executor_client.soundboard_sound_create(
                    guild,
                    sound = data,
                    reason = reason,
                    **fields,
                )
            
            else:
                # No more cases
                pass
        
        except ConnectionError:
            return
        
        except DiscordException as exception:
            if exception.status >= 500:
                return
            
            error_code = exception.code
            # Generic
            if (error_code == ERROR_CODES.missing_access) or (error_code == ERROR_CODES.missing_permissions):
                # Discord drops `missing_permissions` instead of `missing_access` at many cases.
                error_message = 'I was kicked or my permissions changed in the meantime.'
                break
            
            if entity_type is Emoji:
                if error_code == ERROR_CODES.failed_to_resize_asset_below_max_size:
                    error_message = 'Failed to resize asset below max size.'
                    break
                
                if error_code == ERROR_CODES.cannot_mix_subscription_and_non_subscription_roles_for_an_emoji:
                    error_message = 'Cannot mix both subscription and non subscription roles for an emoji.'
                    break
                
                if error_code == ERROR_CODES.max_emojis:
                    error_message = 'Static emoji limit reached.'
                    break
                
                if error_code == ERROR_CODES.max_animated_emojis:
                    error_message = 'Animated emoji limit reached.'
                    break
                
                if error_code == ERROR_CODES.max_premium_emoji:
                    error_message = 'Premium emoji limit reached.'
                    break
            
            elif entity_type is Sticker:
                if error_code == ERROR_CODES.invalid_lottie_json:
                    error_message = 'Invalid lottie json.'
                    break
                
                if error_code == ERROR_CODES.sticker_maximum_dimensions_exceeded:
                    error_message = 'Dimensions exceed the upper threshold (320x320).'
                    break
                
                if error_code == ERROR_CODES.sticker_frame_rate_out_of_expected_range:
                    error_message = 'Frame rate outside of allowed range (?-400ms).'
                    break
                
                if error_code == ERROR_CODES.sticker_animation_duration_exceeds_five_second:
                    error_message = 'Animation duration exceeds the upper threshold (5s).'
                    break
                
                if error_code == ERROR_CODES.max_stickers:
                    error_message = 'Sticker limit reached.'
                    break
            
            elif entity_type is SoundboardSound:
                if error_code == ERROR_CODES.file_type_invalid:
                    error_message = 'File type invalid.'
                    break
                
                if error_code == ERROR_CODES.file_max_duration:
                    error_message = 'File longer than the maximal allowed duration (5.2s).'
                    break
                
                if error_code == ERROR_CODES.max_soundboard_sounds:
                    error_message = 'Soundboard sounds limit reached.'
                    break
            
            raise
        
        content = f'The {get_entity_type_name(entity_type)!s} has been successfully added.'
        
        if interaction_event.type is InteractionType.application_command:
            await client.interaction_response_message_edit(
                interaction_event,
                content = content,
            )
        else:
            await client.interaction_followup_message_create(
                interaction_event,
                content = content,
                show_for_invoking_user_only = True,
            )
        
        return
    
    if interaction_event.type is InteractionType.application_command:
        await client.interaction_response_message_edit(
            interaction_event,
            content = error_message,
        )
    else:
        await client.interaction_followup_message_create(
            interaction_event,
            content = error_message,
            show_for_invoking_user_only = True,
        )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_EDIT_PATTERN, target = 'form')
async def handle_snipe_edit(
    client,
    interaction_event,
    current_entity_packed,
    *,
    name : CUSTOM_ID_ENTITY_NAME = None,
    roles : CUSTOM_ID_ENTITY_ROLES = None,
    tags : CUSTOM_ID_ENTITY_TAGS = None,
    description : CUSTOM_ID_ENTITY_DESCRIPTION = None,
    emoji : CUSTOM_ID_ENTITY_EMOJI = None,
    volume : CUSTOM_ID_ENTITY_VOLUME = None,
    reason : CUSTOM_ID_ENTITY_REASON = None,
):
    """
    Handles a snipe edit interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    current_entity_packed : `str`
        The packed entity.
    
    name : `None | str` = `None`, Optional (Keyword only)
        Inputted name.
    
    roles : ``None | tuple<Role>`` = `None`, Optional (Keyword only)
        Selected roles.
    
    tags : `None | str` = `None`, Optional (Keyword only)
        Inputted tags.
    
    description : `None | str` = `None`, Optional (Keyword only)
        Input description.
    
    emoji : `None | str` = `None`, Optional (Keyword only)
        Input emoji.
    
    volume : `None | str` = `None`, Optional (Keyword only)
        Input volume.
    
    reason : `None | str` = `None`, Optional (Keyword only)
        Input reason.
    """
    if interaction_event.type is InteractionType.application_command:
        await client.interaction_application_command_acknowledge(
            interaction_event,
            False,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_component_acknowledge(
            interaction_event,
            False,
        )
    
    while True:
        # entity & entity_type
        entity = unpack_entity(current_entity_packed)
        if (entity is None):
            error_message = 'Could not recognize the entity to be edited.'
            break
        
        entity_type = type(entity)
        
        # guild
        guild_id = entity.guild_id
        if not guild_id:
            error_message = 'The selected entity is from an unknown guild.'
            break
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            error_message = 'The selected entity is from an unknown guild.'
            break
        
        
        if not has_user_required_permissions(guild, interaction_event.user, PERMISSION_MASK_EXPRESSION_EDIT_OR_DELETE):
            error_message = 'You do not have the required permissions.'
            break
        
        executor_client = get_first_client_with_permissions(guild, PERMISSION_MASK_EXPRESSION_EDIT_OR_DELETE)
        if (executor_client is None):
            error_message = 'I do not have the required permissions.'
            break
        
        # Start building the fields.
        fields = {}
        
        # name
        if (name is not None):
            fields['name'] = name
        
        # roles
        if (entity_type is Emoji) and (interaction_event.guild_id == guild_id):
            identified, role_ids_processed = identify_input_role_ids(roles)
            if not identified:
                error_message = 'Could not recognize the inputted roles.'
                break
            
            if entity.role_ids != role_ids_processed:
                fields['role_ids'] = role_ids_processed
        
        # tags
        if (entity_type is Sticker):
            identified, tags_processed = identify_input_tags(tags)
            if not identified:
                error_message = 'Could not recognize the inputted tags.'
                break
            
            if (tags_processed is None):
                error_message = 'At least one non-empty tag is required'
                break
            
            if entity.tags != tags_processed:
                fields['tags'] = tags_processed
        
        # description
        if (entity_type is Sticker):
            if entity.description != description:
                fields['description'] = description
        
        # emoji
        if (entity_type is SoundboardSound):
            identified, emoji_processed = identify_input_emoji(guild, emoji)
            if not identified:
                error_message = 'Could not recognize the inputted emoji.'
                break
            
            if (
                (emoji_processed is not None) and
                emoji_processed.is_custom_emoji() and
                (emoji_processed.guild_id != guild_id)
            ):
                error_message = 'Emoji of other guilds are not available to be chosen.'
                break
            
            if entity.emoji is not emoji_processed:
                fields['emoji'] = emoji_processed
        
        # volume
        if (entity_type is SoundboardSound):
            if (volume is not None):
                volume = 1.0
            else:
                try:
                    volume = float(volume)
                except ValueError:
                    error_message = 'Invalid volume format.'
                    break
                
                if volume <= 0.0:
                    error_message = 'Volume must be greater than 0.0.'
                    break
                
                if volume > 1.0:
                    error_message = 'Volume must be lower or equal to 1.0.'
                    break
            
            if entity.volume != volume:
                fields['volume'] = volume
        
        try:
            if entity_type is Emoji:
                await executor_client.emoji_edit_guild(
                    entity,
                    reason = reason,
                    **fields,
                )
            
            elif entity_type is Sticker:
                await executor_client.sticker_edit(
                    entity,
                    reason = reason,
                    **fields,
                )
            
            elif entity_type is SoundboardSound:
                await executor_client.soundboard_sound_edit(
                    entity,
                    reason = reason,
                    **fields,
                )
            
            else:
                # No more cases
                pass
        
        except ConnectionError:
            return
        
        except DiscordException as exception:
            if exception.status >= 500:
                return
            
            error_code = exception.code
            # Generic
            if (error_code == ERROR_CODES.missing_access) or (error_code == ERROR_CODES.missing_permissions):
                # Discord drops `missing_permissions` instead of `missing_access` at many cases.
                error_message = 'I was kicked or my permissions changed in the meantime.'
                break
            
            if entity_type is Emoji:
                if error_code == ERROR_CODES.unknown_emoji:
                    error_message = 'The emoji has been deleted.'
                    break
                
                if error_code == ERROR_CODES.cannot_mix_subscription_and_non_subscription_roles_for_an_emoji:
                    error_message = 'Cannot mix both subscription and non subscription roles for an emoji.'
                    break
                
                if error_code == ERROR_CODES.cannot_convert_emoji_between_premium_and_non_premium:
                    error_message = 'Cannot convert emoji between premium and non premium.'
                    break
            
            elif entity_type is Sticker:
                if error_code == ERROR_CODES.unknown_sticker:
                    error_message = 'The sticker has been deleted.'
                    break
                
                pass
            
            elif entity_type is SoundboardSound:
                # No unknown soundboard sound?
                pass
            
            raise
        
        content = f'The {get_entity_type_name(entity_type)!s} has been successfully edited.'
        
        if interaction_event.type is InteractionType.application_command:
            await client.interaction_response_message_edit(
                interaction_event,
                content = content,
            )
        else:
            await client.interaction_followup_message_create(
                interaction_event,
                content = content,
                show_for_invoking_user_only = True,
            )
        
        return
    
    if interaction_event.type is InteractionType.application_command:
        await client.interaction_response_message_edit(
            interaction_event,
            content = error_message,
        )
    else:
        await client.interaction_followup_message_create(
            interaction_event,
            content = error_message,
            show_for_invoking_user_only = True,
        )
    return


@FEATURE_CLIENTS.interactions(custom_id = CUSTOM_ID_SNIPE_REMOVE_PATTERN, target = 'form')
async def handle_snipe_remove(
    client,
    interaction_event,
    current_entity_packed,
    *,
    reason : CUSTOM_ID_ENTITY_REASON = None,
):
    """
    Handles a snipe remove interaction.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client receiving the interaction.
    
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    current_entity_packed : `str`
        The packed entity.
    
    reason : `None | str` = `None`, Optional (Keyword only)
        Input reason.
    """
    if interaction_event.type is InteractionType.application_command:
        await client.interaction_application_command_acknowledge(
            interaction_event,
            False,
            show_for_invoking_user_only = True,
        )
    else:
        await client.interaction_component_acknowledge(
            interaction_event,
            False,
        )
    
    while True:
        # entity & entity_type
        entity = unpack_entity(current_entity_packed)
        if (entity is None):
            error_message = 'Could not recognize the entity to be edited.'
            break
        
        entity_type = type(entity)
        
        # guild
        guild_id = entity.guild_id
        if not guild_id:
            error_message = 'The selected entity is from an unknown guild.'
            break
        
        try:
            guild = GUILDS[guild_id]
        except KeyError:
            error_message = 'The selected entity is from an unknown guild.'
            break
        
        
        if not has_user_required_permissions(guild, interaction_event.user, PERMISSION_MASK_EXPRESSION_EDIT_OR_DELETE):
            error_message = 'You do not have the required permissions.'
            break
        
        executor_client = get_first_client_with_permissions(guild, PERMISSION_MASK_EXPRESSION_EDIT_OR_DELETE)
        if (executor_client is None):
            error_message = 'I do not have the required permissions.'
            break
        
        try:
            if entity_type is Emoji:
                await executor_client.emoji_delete_guild(
                    entity,
                    reason = reason,
                )
            
            elif entity_type is Sticker:
                await executor_client.sticker_delete(
                    entity,
                    reason = reason,
                )
            
            elif entity_type is SoundboardSound:
                await executor_client.soundboard_sound_delete(
                    entity,
                    reason = reason,
                )
            
            else:
                # No more cases
                pass
        
        except ConnectionError:
            return
        
        except DiscordException as exception:
            if exception.status >= 500:
                return
            
            error_code = exception.code
            # Generic
            if (error_code == ERROR_CODES.missing_access) or (error_code == ERROR_CODES.missing_permissions):
                # Discord drops `missing_permissions` instead of `missing_access` at many cases.
                error_message = 'I was kicked or my permissions changed in the meantime.'
                break
            
            if entity_type is Emoji:
                if error_code == ERROR_CODES.unknown_emoji:
                    error_message = 'The emoji has been removed.'
                    break
            
            elif entity_type is Sticker:
                if error_code == ERROR_CODES.unknown_sticker:
                    error_message = 'The sticker has been removed.'
                    break
                
                pass
            
            elif entity_type is SoundboardSound:
                # No unknown soundboard sound?
                pass
            
            raise
        
        content = f'The {get_entity_type_name(entity_type)!s} has been successfully removed.'
        
        if interaction_event.type is InteractionType.application_command:
            await client.interaction_response_message_edit(
                interaction_event,
                content = content,
            )
        else:
            await client.interaction_followup_message_create(
                interaction_event,
                content = content,
                show_for_invoking_user_only = True,
            )
        
        return
    
    if interaction_event.type is InteractionType.application_command:
        await client.interaction_response_message_edit(
            interaction_event,
            content = error_message,
        )
    else:
        await client.interaction_followup_message_create(
            interaction_event,
            content = error_message,
            show_for_invoking_user_only = True,
        )
    return
