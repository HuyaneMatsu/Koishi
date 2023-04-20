__all__ = ()

import re

from hata import StickerType, StickerFormat, parse_role

from .helpers import propagate_check_error_message


def process_reason(event, reason):
    """
    Processes the given reason.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interactions event.
    reason : `None`, `str`
        Reason given.
    
    Returns
    -------
    reason : `str`
    """
    reason_parts = []
    if (reason is not None):
        reason_parts.append(reason)
        reason_parts.append('\n')
    
    caller = event.user
    reason_parts.append('Requested by: ')
    reason_parts.append(caller.full_name)
    reason_parts.append(' [')
    reason_parts.append(str(caller.id))
    reason_parts.append(']')
    
    return ''.join(reason_parts)


async def check_emoji_type(client, event, emoji):
    """
    Checks the emoji's type.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    emoji : ``Emoji``
        The emoji in context.
    
    Returns
    -------
    passed : `bool`
        Whether all checks passed.
    """
    if not emoji.is_custom_emoji():
        await propagate_check_error_message(client, event, 'Cannot execute action on non-custom emoji.')
        return False
    
    return True


async def check_emoji_guild(client, event, emoji):
    """
    Checks whether the emoji's guild is the event's.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    emoji : ``Emoji``
        The emoji in context.
    
    Returns
    -------
    passed : `bool`
        Whether all checks passed.
    """
    guild_id = emoji.guild_id
    if (guild_id == 0) or (guild_id != event.guild_id):
        await propagate_check_error_message(
            client, event, 'Cannot perform the action on an emoji from an other guild.'
        )
        return False
    
    return True



async def check_sticker_type_create(client, event, sticker):
    """
    Checks sticker type for creation.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    sticker : ``Sticker``
        The sticker in context.
    
    Returns
    -------
    passed : `bool`
        Whether all checks passed.
    """
    if sticker.format is StickerFormat.lottie:
        await propagate_check_error_message(client, event, 'Cannot execute action on lottie sticker.')
        return False
    
    return True


async def check_sticker_type_modify(client, event, sticker):
    """
    Checks sticker type for modification / deletion.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    sticker : ``Sticker``
        The sticker in context.
    
    Returns
    -------
    passed : `bool`
        Whether all checks passed.
    """
    if sticker.type is not StickerType.guild:
        await propagate_check_error_message(client, event, 'Cannot execute action on non-guild sticker.')
        return False
    
    return True


async def check_sticker_guild(client, event, sticker):
    """
    Checks whether the sticker's guild is the event's.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    sticker : ``Sticker``
        The sticker in context.
    
    Returns
    -------
    passed : `bool`
        Whether all checks passed.
    """
    guild_id = sticker.guild_id
    if (guild_id == 0) or (guild_id != event.guild_id):
        await propagate_check_error_message(
            client, event, 'Cannot perform the action on a sticker from an other guild.'
        )
        return False
    
    return True


def produce_limit_error_message(count, limit, name):
    """
    Checks the whether the limits are fine. If not returns an error message.
    
    Parameters
    ----------
    count : `int`
        The current entity count.
    limit : `int`
        The maximal available entity count.
    name : `str`
        The entity's name.
    
    Returns
    -------
    error_message : `None`, `str`
    """
    if count >= limit:
        return f'The guild has no free {name} slots. **{count} used** out of **{limit} available**.'


async def check_emoji_counts(client, event, emoji):
    """
    Checks whether there are available emoji spaces in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    emoji : ``Emoji``
        The emoji in context.
    
    Returns
    -------
    passed : `bool`
    """
    guild = event.guild
    if guild is None:
        return False
    
    emoji_counts = guild.emoji_counts
    
    if emoji.animated:
        count = emoji_counts.normal_animated
        name = 'animated emoji'
    
    else:
        count = emoji_counts.normal_static
        name = 'static emoji'
    
    error_message = produce_limit_error_message(count, guild.emoji_limit, name)
    if (error_message is not None):
        await propagate_check_error_message(client, event, error_message)
        return False
    
    return True


async def check_sticker_counts(client, event):
    """
    Checks whether there are available sticker spaces in the guild.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    passed : `bool`
    """
    guild = event.guild
    if guild is None:
        return False
    
    error_message = produce_limit_error_message(len(guild.stickers), guild.sticker_limit, 'sticker')
    if (error_message is not None):
        await propagate_check_error_message(client, event, error_message)
        return False
    
    return True


def is_character_allowed_in_emoji(character):
    """
    Returns whether the character is allowed in an emoji name.
    
    Parameters
    ----------
    character : `str`
        The character to check
    
    Returns
    -------
    is_allowed : `bool`
    """
    character = ord(character)
    if (character >= b'a'[0]) and (character <= b'z'[0]):
        return True

    if (character >= b'A'[0]) and (character <= b'Z'[0]):
        return True
    
    if (character >= b'0'[0]) and (character <= b'9'[0]):
        return True
    
    if (character == b'_'[0]):
        return True
    
    return False


def get_emoji_name_invalid_character_indexes(emoji_name):
    """
    Gets which characters are invalid in the emoji's name.
    
    Parameters
    ----------
    emoji_name : `str`
        The emoji name to check.
    
    Returns
    -------
    invalid_character_indexes : `None`, `set` of `int`
    """
    invalid_character_indexes = None
    
    for index, character in enumerate(emoji_name):
        if is_character_allowed_in_emoji(character):
            continue
        
        if (invalid_character_indexes is None):
            invalid_character_indexes = set()
        
        invalid_character_indexes.add(index)
        continue
    
    return invalid_character_indexes


def build_emoji_name_invalid_message(emoji_name, invalid_character_indexes):
    """
    Builds an error message for the case when any of the emoji name's characters are invalid.
    
    Parameters
    ----------
    emoji_name : `str`
        The emoji name in context.
    invalid_character_indexes : `set` of `int`
        The invalid character's indexes.
    
    Returns
    -------
    error_message : `str`
    """
    error_message_parts = [
        'Invalid characters in emoji name:\n```\n',
        emoji_name,
        '\n'
    ]
    
    for index in range(len(emoji_name)):
        if index in invalid_character_indexes:
            sign = '^'
        else:
            sign = ' '
        
        error_message_parts.append(sign)
    
    error_message_parts.append('\n```')
    
    return ''.join(error_message_parts)


async def check_is_emoji_name_valid(client, event, emoji_name):
    """
    Checks whether the given emoji name contains invalid characters.
    
    This function is a coroutine.
    
    Parameters
    ----------
    client : ``Client``
        The client who received the event.
    event : ``InteractionEvent``
        The received interaction event.
    
    Returns
    -------
    passed : `bool`
    """
    invalid_character_indexes = get_emoji_name_invalid_character_indexes(emoji_name)
    if (invalid_character_indexes is None):
        return True
    
    error_message = build_emoji_name_invalid_message(emoji_name, invalid_character_indexes)
    await propagate_check_error_message(client, event, error_message)
    return False


def join_sticker_tags(sticker):
    """
    Joins the given sticker's tags.
    
    Parameters
    ----------
    sticker : ``Sticker``
        The sticker to join its tags of.
    
    Returns
    -------
    joined_tags : `str`
    """
    tags = sticker.tags
    if tags is None:
        return ''
    
    return ', '.join(sorted(tags))


TAG_PATTERN = re.compile('\\w+')

def parse_and_join_tags(raw_tags):
    """
    Parses the given tags and joins them.
    
    Parameters
    ----------
    tags : `str`
        Tags to join.
    
    Returns
    -------
    joined_tags : `str`
    """
    return ', '.join(TAG_PATTERN.findall(raw_tags))


def join_roles(roles):
    """
    Joins the given roles.
    
    Parameters
    ----------
    roles : `None`, `iterable` of ``Role``
        The roles to join.
    
    Returns
    -------
    joined_roles : `str`
    """
    if roles is None:
        return ''
    
    return ', '.join([role.name for role in roles])


def parse_roles(raw_roles, guild):
    """
    Parses the roles in the given context.
    
    Parameters
    ----------
    raw_roles : `None`, `str`
        The raw roles to parse.
    guild : ``Guild``, ``None``
        The guild to look the role up for in at the case of name based parsing.
    
    Returns
    -------
    roles : `list` of ``Role``
        The parsed roles.
    """
    return [
        role for role in
        (
            parse_role(value, guild) for value in (
                value.strip() for value in raw_roles.split(',')
            ) if value
        ) if role is not None
    ]
