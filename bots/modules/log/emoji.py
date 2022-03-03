from hata import Client, Embed, StickerFormat, DATETIME_FORMAT_CODE, DiscordException, ERROR_CODES, ROLES, ZEROUSER
from hata.ext.extension_loader import require

from bot_utils.constants import CHANNEL__SUPPORT__LOG_EMOJI, GUILD__SUPPORT

require('Satori')

Satori: Client


def get_role_name(role_id):
    try:
        role = ROLES[role_id]
    except KeyError:
        role_name = str(role_id)
    else:
        role_name = role.name
    
    return role_name


def add_role_names_to_description_parts(role_ids, description_parts, truncate, truncate_at):
    if (role_ids is None):
        description_parts.append('null\n')
    else:
        if truncate:
            truncated = len(role_ids) - truncate_at
            if truncated < 0:
                truncated = 0
            else:
                role_ids = role_ids[:truncate_at]
        else:
            truncated = 0
        
        for role_id in role_ids:
            description_parts.append(get_role_name(role_id))
            description_parts.append('\n')
        
        if truncated:
            description_parts.append(str(truncated))
            description_parts.append(' truncated ...\n')


def create_modified_string_field_description(old_value, new_value):
    return (
        f'```\n'
        f'{old_value} -> {new_value}\n'
        f'```'
    )

def get_bool_repr(value):
    return 'true' if value else 'false'


def get_preinstanced_repr(value):
    return f'{value.name} ({value.value})'


def get_nullable_container_repr(value):
    return 'null' if value is None else ''.join([repr(element) for element in value])


def get_nullable_string_repr(value):
    return 'null' if value is None else value


def add_modified_string_field(embed, name, old_value, new_value):
    return embed.add_field(
        name,
        create_modified_string_field_description(old_value, new_value),
    )


def try_get_modified_difference(entity, old_attributes, attribute_name):
    try:
        old_value = old_attributes[attribute_name]
    except KeyError:
        difference = None
    else:
        new_value = getattr(entity, attribute_name)
        
        difference = old_value, new_value
    
    return difference


def maybe_add_modified_string_field(embed, entity, old_attributes, attribute_name, pretty_name):
    return _maybe_add_difference_field(embed, entity, old_attributes, attribute_name, pretty_name, None)


def _maybe_add_difference_field(embed, entity, old_attributes, attribute_name, pretty_name, converter):
    difference = try_get_modified_difference(entity, old_attributes, attribute_name)
    if (difference is not None):
        old_value, new_value = difference
        
        if (converter is not None):
            old_value = converter(old_value)
            new_value = converter(new_value)
        
        embed = add_modified_string_field(
            embed,
            pretty_name,
            old_value,
            new_value,
        )
    return embed

def maybe_add_modified_bool_field(embed, entity, old_attributes, attribute_name, pretty_name):
    return _maybe_add_difference_field(embed, entity, old_attributes, attribute_name, pretty_name, get_bool_repr)


def maybe_add_modified_nullable_string_field(embed, entity, old_attributes, attribute_name, pretty_name):
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_nullable_string_repr,
)

def maybe_add_modified_nullable_container_field(embed, entity, old_attributes, attribute_name, pretty_name):
    return _maybe_add_difference_field(
        embed,
        entity,
        old_attributes,
        attribute_name,
        pretty_name,
        get_nullable_container_repr,
)

def add_string_field(embed, value, pretty_name):
    return embed.add_field(
        pretty_name,
        (
            f'```\n'
            f'{value}\n'
            f'```'
        ),
    )


def add_bool_field(embed, value, pretty_name):
    return add_string_field(embed, get_bool_repr(value), pretty_name)


def add_preinstanced_field(embed, value, pretty_name):
    return add_string_field(embed, get_preinstanced_repr(value), pretty_name)


def add_nullable_container_field(embed, value, pretty_name):
    return add_string_field(embed, get_preinstanced_repr(value), pretty_name)


def add_nullable_string_field(embed, value, pretty_name):
    return add_string_field(embed, get_nullable_string_repr(value), pretty_name)


def add_emoji_fields_to(emoji, embed):
    add_string_field(embed, emoji.name, 'Name')
    add_bool_field(embed, emoji.animated, 'Animated')
    add_bool_field(embed, emoji.available, 'Available')
    
    
    description_parts = ['```\n']
    
    role_ids = emoji.role_ids
    if (role_ids is None):
        description_parts.append('null\n')
    else:
        add_role_names_to_description_parts(role_ids, description_parts, True, 8)
    description_parts.append('```')
    
    description = ''.join(description_parts)
    description_parts = None
    
    embed.add_field(
        'Allowed roles',
        description,
    )
    
    add_bool_field(embed, emoji.managed, 'Managed')
    add_bool_field(embed, emoji.require_colons, 'Require colons')
    
    return embed


def add_creator_field_to(entity, embed):
    created_at_string = format(entity.created_at, DATETIME_FORMAT_CODE)
    user = entity.user
    if user is ZEROUSER:
        footer_text = created_at_string
        icon_url = None
    else:
        footer_text = f'{user.full_name} | {created_at_string}'
        icon_url = user.avatar_url
    
    return embed.add_footer(footer_text, icon_url)


@Satori.events
async def emoji_create(client, emoji):
    if emoji.guild_id != GUILD__SUPPORT.id:
        return
    
    # We get the creator of the emoji.
    try:
        await client.emoji_get(emoji, force_update=True)
    except ConnectionError:
        # No internet connection
        return
    
    except DiscordException as err:
        # Sticker already deleted?
        if err.code != ERROR_CODES.unknown_emoji:
            raise
    
    emoji_url = emoji.url
    
    embed = Embed(f'Emoji created: {emoji.name} ({emoji.id})', url=emoji_url).add_thumbnail(emoji_url)
    add_emoji_fields_to(emoji, embed)
    add_creator_field_to(emoji, embed)
    
    await client.message_create(CHANNEL__SUPPORT__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def emoji_edit(client, emoji, old_attributes):
    if emoji.guild_id != GUILD__SUPPORT.id:
        return
    
    
    emoji_url = emoji.url
    
    embed = Embed(f'Emoji edited: {emoji.name} ({emoji.id})', url=emoji_url).add_thumbnail(emoji_url)
    add_creator_field_to(emoji, embed)
    
    maybe_add_modified_string_field(embed, emoji, old_attributes, 'name', 'name')
    
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'animated', 'Animated')
    
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'available', 'Available')
    
    try:
        old_role_ids = old_attributes['role_ids']
    except KeyError:
        pass
    else:
        new_role_ids = emoji.role_ids
        
        total_role_count = 0
        if (old_role_ids is not None):
            total_role_count += len(old_role_ids)
        
        if (new_role_ids is not None):
            total_role_count += len(new_role_ids)
        
        truncate = (total_role_count > 8)
        
        description_parts = ['```\n']
        
        add_role_names_to_description_parts(old_role_ids, description_parts, truncate, 4)
        description_parts.append('->\n')
        add_role_names_to_description_parts(new_role_ids, description_parts, truncate, 4)
        
        description_parts.append('```')
        
        description = ''.join(description_parts)
        description_parts = None
        
        embed.add_field(
            'Allowed roles',
            description,
        )
    
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'managed', 'Managed')
    
    maybe_add_modified_bool_field(embed, emoji, old_attributes, 'require_colons', 'Require colons')
    
    await client.message_create(CHANNEL__SUPPORT__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def emoji_delete(client, emoji):
    if emoji.guild_id != GUILD__SUPPORT.id:
        return
    
    embed = Embed(f'Emoji deleted: {emoji.name} ({emoji.id})')
    embed = add_emoji_fields_to(emoji, embed)
    
    await client.message_create(CHANNEL__SUPPORT__LOG_EMOJI, embed=embed, allowed_mentions=None)


def add_sticker_fields_to(sticker, embed):
    description_parts = []
    
    add_string_field(embed, sticker.name, 'Name')
    add_nullable_string_field(embed, sticker.description, 'Description')
    add_preinstanced_field(embed, sticker.format, 'Format')
    add_bool_field(embed, sticker.available, 'Available')
    add_nullable_container_field(embed, sticker.tags, 'Tags')
    
    return embed


@Satori.events
async def sticker_create(client, sticker):
    if sticker.guild_id != GUILD__SUPPORT.id:
        return
    
    # We get the creator of the sticker.
    try:
        await client.sticker_guild_get(sticker, force_update=True)
    except ConnectionError:
        # No internet connection
        return
    
    except DiscordException as err:
        # Sticker already deleted?
        if err.code != ERROR_CODES.unknown_sticker:
            raise
    
    sticker_url = sticker.url
    
    embed = Embed(f'Sticker created: {sticker.name} ({sticker.id})', url=sticker_url)
    add_sticker_fields_to(sticker, embed)
    add_creator_field_to(sticker, embed)
    
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker_url)
    
    await client.message_create(CHANNEL__SUPPORT__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def sticker_edit(client, sticker, old_attributes):
    if sticker.guild_id != GUILD__SUPPORT.id:
        return
    
    sticker_url = sticker.url
    embed = Embed(f'Sticker edited: {sticker.name} ({sticker.id})', url=sticker_url)
    add_creator_field_to(sticker, embed)
    
    maybe_add_modified_string_field(embed, sticker, old_attributes, 'name', 'name')
    maybe_add_modified_nullable_string_field(embed, sticker, old_attributes, 'description', 'Description')
    maybe_add_modified_bool_field(embed, sticker, old_attributes, 'available', 'Available')
    maybe_add_modified_nullable_container_field(embed, sticker, old_attributes, 'tags', 'Tags')
    
    sticker_format = sticker.format
    if (sticker_format is StickerFormat.png) or (sticker_format is StickerFormat.apng):
        embed.add_image(sticker_url)
    
    await client.message_create(CHANNEL__SUPPORT__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events
async def sticker_delete(client, sticker):
    if sticker.guild_id != GUILD__SUPPORT.id:
        return
    
    embed = Embed(f'Sticker deleted: {sticker.name} ({sticker.id})')
    add_sticker_fields_to(sticker, embed)
    add_creator_field_to(sticker, embed)
    
    await client.message_create(CHANNEL__SUPPORT__LOG_EMOJI, embed=embed, allowed_mentions=None)


@Satori.events(name='ready')
async def initial_request_stickers(client):
    try:
        await client.sticker_guild_get_all(GUILD__SUPPORT)
    except ConnectionError:
        # No internet connection
        return

    client.events.remove(initial_request_stickers, name='ready')

@Satori.events(name='ready')
async def initial_request_emmojis(client):
    try:
        await client.emoji_guild_get_all(GUILD__SUPPORT)
    except ConnectionError:
        # No internet connection
        return
    
    client.events.remove(initial_request_emmojis, name='ready')
