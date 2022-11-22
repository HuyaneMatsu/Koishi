__all__ = ()

import re

from hata import Client, ComponentType, DiscordException, EMOJIS, ERROR_CODES, Emoji, ZEROUSER
from hata.ext.slash import Form, TextInput, TextInputStyle

from .constants import (
    BUTTON_SNIPE_ADD_DISABLED, BUTTON_SNIPE_DM_DISABLED, CUSTOM_ID_SNIPE_ADD_EMOJI, CUSTOM_ID_SNIPE_ADD_STICKER,
    CUSTOM_ID_SNIPE_CLOSE, CUSTOM_ID_SNIPE_DM, CUSTOM_ID_SNIPE_INFO_EMOJI, CUSTOM_ID_SNIPE_INFO_STICKER,
    create_emoji_add_form_custom_id, EMOJI_FORM_PATTERN, create_sticker_add_form_custom_id, STICKER_FORM_PATTERN
)
from .emoji_info import get_emoji_info
from .lister_helpers import create_base_embed
from .sticker_helpers import get_sticker
from .sticker_info import get_sticker_info


MATCH_ID_IN_FIELD_VALUE = re.compile('[0-9]+')
MATCH_NAME_IN_FIELD_VALUE = re.compile('[0-9a-zA-Z_\-]+')

SLASH_CLIENT : Client

DISABLED_TABLE_DM = {
    CUSTOM_ID_SNIPE_ADD_EMOJI: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_ADD_STICKER: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_DM: BUTTON_SNIPE_DM_DISABLED,
}

DISABLED_TABLE_ADD = {
    CUSTOM_ID_SNIPE_ADD_EMOJI: BUTTON_SNIPE_ADD_DISABLED,
    CUSTOM_ID_SNIPE_ADD_STICKER: BUTTON_SNIPE_ADD_DISABLED,
}


def disable_guild_only_buttons(component):
    return disable_common(component, DISABLED_TABLE_DM)


def disable_add_buttons(component):
    return disable_common(component, DISABLED_TABLE_ADD)


def disable_common(component, table):
    if component.type is ComponentType.row:
        return [table.get(sub_component.custom_id, sub_component) for sub_component in component]
    
    return component


def get_entity_id_from_event_message(event):
    message = event.message
    if message is None:
        return 0
    
    embed = message.embed
    if embed is None:
        return 0
    
    fields = embed.fields
    if (fields is None) or len(fields) < 2:
        return 0
    
    field = fields[1]
    match = MATCH_ID_IN_FIELD_VALUE.search(field.value)
    if match is None:
        return 0
    
    return int(match.group(0))


def get_emoji_animated_and_name_from_event_message(event):
    embed = event.message.embed
    
    url = embed.url
    if url is None:
        animated = False
    else:
        animated = url.endswith('.gif')
    
    field = event.message.embed.fields[0]
    match = MATCH_NAME_IN_FIELD_VALUE.search(field.value)
    if match is None:
        name = ''
    else:
        name = match.group(0)
        
    return animated, name


def get_emoji_from_event(event):
    emoji_id = get_entity_id_from_event_message(event)
    if emoji_id == 0:
        return
    
    emoji = EMOJIS.get(emoji_id, None)
    if emoji is not None:
        return emoji
    
    animated, name = get_emoji_animated_and_name_from_event_message(event)
    return Emoji._create_partial(int(emoji_id), name, animated)


async def get_sticker_from_event(client, event):
    sticker_id = get_entity_id_from_event_message(event)
    if sticker_id:
        return await get_sticker(client, sticker_id)


def copy_information_fields(event, response_embed):
    embed = event.message.embed
    response_embed.author = embed.author
    response_embed.footer = embed.footer


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_DM)
async def snipe_message_dm(client, event):
    await client.interaction_component_acknowledge(event, wait = False)
    
    message = event.message
    if message is None:
        return
    
    embed = message.embed
    if embed is None:
        return
    
    components = [disable_guild_only_buttons(component) for component in message.iter_components()]
    
    channel = await client.channel_private_create(event.user)
    
    try:
        await client.message_create(channel, embed = embed, components = components)
    except DiscordException as err:
        if err.code == ERROR_CODES.cannot_message_user: # user has dm-s disabled:
            await client.interaction_followup_message_create(
                event,
                'Could not deliver direct message.',
                show_for_invoking_user_only = True
            )
        
        else:
            raise


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_INFO_EMOJI)
async def show_emoji_info(client, event):
    await client.interaction_component_acknowledge(event, wait = False)
    
    emoji = get_emoji_from_event(event)
    if (emoji is None):
        return
    
    guild = emoji.guild
    if emoji.is_custom_emoji():
        if (emoji.user is ZEROUSER) and (guild is not None) and (guild in client.guilds) and (not emoji.managed):
            try:
                await client.emoji_get(emoji, force_update = True)
            except DiscordException as err:
                if err.code not in (
                    ERROR_CODES.missing_access, # Client removed.
                ):
                    raise
    
    response_embed = get_emoji_info(emoji)
    copy_information_fields(event, response_embed)
    
    await client.interaction_followup_message_create(
        event,
        embed = response_embed,
        show_for_invoking_user_only = bool(event.guild_id),
    )



@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_INFO_STICKER)
async def show_sticker_info(client, event):
    await client.interaction_component_acknowledge(event, wait = False)
    
    sticker = await get_sticker_from_event(client, event)
    if sticker is None:
        return
    
    response_embed = get_sticker_info(event, sticker)
    copy_information_fields(event, response_embed)
    
    await client.interaction_followup_message_create(
        event,
        embed = response_embed,
        show_for_invoking_user_only = bool(event.guild_id),
    )


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_CLOSE)
async def close_message(client, event):
    await client.interaction_component_acknowledge(event, wait = False)
    
    message = event.message
    if message is None:
        return
    
    if event.guild_id == 0:
        delete = True
    
    elif event.user_permissions.can_manage_messages:
        delete = True
    
    else:
        interaction = message.interaction
        if interaction is None:
            delete = True
        
        elif interaction.user is event.user:
            delete = True
        
        else:
            delete = False
    
    
    if not delete:
        await client.interaction_followup_message_create(
            event,
            'You must be the invoker of the interaction, or have manage messages permission to do this.',
            show_for_invoking_user_only = True,
        )
        return
    
    try:
        await client.interaction_response_message_delete(event)
    except ConnectionError:
        pass
    
    except DiscordException as err:
        if err.code not in (
            ERROR_CODES.unknown_message, # message deleted
            ERROR_CODES.unknown_channel, # message's channel deleted
            ERROR_CODES.missing_access, # client removed
        ):
            raise


def check_shared_requirements(client, event):
    if not event.user_permissions.can_manage_emojis_and_stickers:
        return 'You are required to have manager emojis & sticker permission to invoke this action.'
    
    guild = event.guild
    if (guild is None) or (not guild.cached_permissions_for(client).can_manage_emojis_and_stickers):
        return 'I required to have manager emojis & sticker permission to execute this action.'
    
    return None


def check_limit(name, count, limit):
    if count >= limit:
        return f'The guild has no free {name} slots. {count} used out of {limit} available.'


def check_emoji_requirements(guild, emoji):
    if emoji.animated:
        count = sum(emoji.animated for emoji in guild.emojis.values())
        name = 'static emoji'
    
    else:
        count = sum((not emoji.animated) for emoji in guild.emojis.values())
        name = 'animated emoji'
    
    return check_limit(name, count, guild.emoji_limit)
    

def check_sticker_requirements(guild, sticker):
    return check_limit('sticker', len(guild.stickers), guild.sticker_limit)



@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_ADD_EMOJI)
async def add_emoji(client, event):
    while True:
        error_message = check_shared_requirements(client, event)
        if error_message is not None:
            break
        
        emoji = get_emoji_from_event(event)
        if emoji is None:
            error_message = 'Failed to re-parse emoji.'
            break
        
        error_message = check_emoji_requirements(event.guild, emoji)
        break
    
    
    if (error_message is not None):
        await client.interaction_component_acknowledge(event)
        await client.interaction_followup_message_create(
            event,
            error_message,
            show_for_invoking_user_only = True,
        )
        return
    
    
    return Form(
        f'Add emoji: {emoji.name}',
        [
            TextInput(
                'Name',
                min_length = 2,
                max_length = 32,
                custom_id = 'name',
                placeholder = 'Emoji name',
                value = emoji.name,
            )
        ],
        custom_id = create_emoji_add_form_custom_id(emoji)
    )


@SLASH_CLIENT.interactions(custom_id = EMOJI_FORM_PATTERN, target = 'form')
async def add_emoji(client, event, emoji_id, emoji_name, emoji_animated, *, name):
    await client.interaction_component_acknowledge(event, wait = False)
    
    emoji = Emoji._create_partial(int(emoji_id), emoji_name, True if emoji_animated == '1' else False)
    
    if name is None:
        name = emoji.name
    
    async with client.http.get(emoji.url) as response:
        data = await response.read()
    
    try:
        new_emoji = await client.emoji_create(event.guild_id, name = name, image = data)
    except ConnectionError:
        return
    
    except DiscordException as err:
        error_code = err.code
        
        if error_code == ERROR_CODES.missing_access:
            return
        
        elif error_code == ERROR_CODES.missing_permissions:
            # Discord can drop this even if the client was removed. How stupid!
            guild = event.guild
            if (guild is None) or (guild not in client.guilds):
                return
            
            error_message = 'Missing permissions.'
        
        elif error_code == ERROR_CODES.invalid_form_body:
            error_message = '\n'.join(err.errors)
        
        elif error_code == ERROR_CODES.failed_to_resize_asset_below_max_size:
            error_message = 'Failed to resize emoji below max size.'
        
        elif error_code == ERROR_CODES.max_emojis:
            error_message = 'Emoji limit hit.'
        
        else:
            raise
        
        await client.interaction_followup_message_create(
            event,
            error_message,
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_followup_message_create(
        event,
        embed = create_base_embed(new_emoji, 'Emoji added'),
        show_for_invoking_user_only = True,
    )
    
    await client.interaction_followup_message_edit(
        event,
        event.message,
        components = [disable_add_buttons(component) for component in event.message.iter_components()],
    )


def join_sticker_tags(sticker):
    tags = sticker.tags
    if tags is None:
        return ''
    
    return ', '.join(sorted(tags))


TAG_PATTERN = re.compile('\\w+')


@SLASH_CLIENT.interactions(custom_id = CUSTOM_ID_SNIPE_ADD_STICKER)
async def add_sticker(client, event):
    while True:
        error_message = check_shared_requirements(client, event)
        if error_message is not None:
            break
        
        sticker = await get_sticker_from_event(client, event)
        if sticker is None:
            error_message = 'Failed to re-parse sticker.'
            break
        
        error_message = check_sticker_requirements(event.guild, sticker)
        break
    
    
    if (error_message is not None):
        await client.interaction_component_acknowledge(event)
        await client.interaction_followup_message_create(
            event,
            error_message,
            show_for_invoking_user_only = True,
        )
        return
    
    
    return Form(
        f'Add sticker: {sticker.name}',
        [
            TextInput(
                'Name',
                min_length = 2,
                max_length = 32,
                custom_id = 'name',
                placeholder = 'Sticker name',
                value = sticker.name,
            ),
            TextInput(
                'Tags',
                min_length = 0,
                max_length = 100,
                custom_id = 'tags',
                placeholder = 'Sticker tags',
                value = join_sticker_tags(sticker),
            ),
            TextInput(
                'Description',
                min_length = 0,
                max_length = 1024,
                custom_id = 'description',
                placeholder = 'Sticker description',
                value = sticker.description,
                style = TextInputStyle.paragraph,
            ),
        ],
        custom_id = create_sticker_add_form_custom_id(sticker)
    )


@SLASH_CLIENT.interactions(custom_id = STICKER_FORM_PATTERN, target = 'form')
async def add_sticker(client, event, sticker_id, *, name, tags, description):
    await client.interaction_component_acknowledge(event, wait = False)
    
    sticker = await get_sticker(client, int(sticker_id))
    
    if name is None:
        name = sticker.name
    
    if tags is None:
        tags = join_sticker_tags(sticker)
    else:
        tags = ', '.join(TAG_PATTERN.findall(tags))
    
    async with client.http.get(sticker.url) as response:
        data = await response.read()
    
    try:
        new_sticker = await client.sticker_guild_create(
            event.guild_id,
            name = name,
            image = data,
            tags = tags,
            description = description,
        )
    except ConnectionError:
        return
    
    except DiscordException as err:
        error_code = err.code
        
        if error_code == ERROR_CODES.missing_access:
            return
        
        elif error_code == ERROR_CODES.missing_permissions:
            # Discord can drop this even if the client was removed. How stupid!
            guild = event.guild
            if (guild is None) or (guild not in client.guilds):
                return
            
            error_message = 'Missing permissions.'
        
        elif error_code == ERROR_CODES.invalid_form_body:
            error_message = '\n'.join(err.errors)
        
        elif error_code == ERROR_CODES.failed_to_resize_asset_below_max_size:
            error_message = 'Failed to resize sticker below max size.'
        
        elif error_code == ERROR_CODES.max_stickers:
            error_message = 'Sticker limit hit.'
        
        else:
            raise
        
        await client.interaction_followup_message_create(
            event,
            error_message,
            show_for_invoking_user_only = True,
        )
        return
    
    await client.interaction_followup_message_create(
        event,
        embed = create_base_embed(new_sticker, 'Sticker added'),
        show_for_invoking_user_only = True,
    )
    
    await client.interaction_followup_message_edit(
        event,
        event.message,
        components = [disable_add_buttons(component) for component in event.message.iter_components()],
    )
