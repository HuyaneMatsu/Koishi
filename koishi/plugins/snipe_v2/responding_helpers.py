__all__ = ()

from itertools import islice

from hata import (
    BUILTIN_EMOJIS, ChannelType, ComponentType, Emoji, SoundboardSound, Sticker, StickerFormat, UNICODE_TO_EMOJI,
    is_id, parse_custom_emojis_ordered, parse_emoji
)

from ...bot_utils.response_data_streaming import create_http_stream_resource

from .caching import get_sticker, request_soundboard_sounds_of
from .constants import FEATURE_FLAG_DETAILED, FEATURE_FLAG_DM, FEATURE_FLAG_REVEALED
from .custom_ids import CUSTOM_ID_SNIPE_CHOICE_BUILDER
from .entity_packing import unpack_entity


def get_attachment_file(client, entity):
    """
    Return the attachment file to send as a response.
    
    Parameters
    ----------
    client : ``Client``
        The client responding.
    
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity being shown.
    
    Returns
    -------
    file : ``None | (str, ResourceStreamFunction)``
    """
    entity_type = type(entity)
    if entity_type is Emoji:
        file = None
    
    elif entity_type is Sticker:
        if entity.format is StickerFormat.lottie:
            file = ('structure.json', create_http_stream_resource(client.http, entity.url))
        
        else:
            file = None
    
    elif entity_type is SoundboardSound:
        file = ('sound.mp3', create_http_stream_resource(client.http, entity.url))
    
    else:
        file = None
    
    return file


def pack_feature_flags(interaction_event, detailed, reveal):
    """
    Packs the given flags.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    detailed : `bool`
        Whether a detailed view of the entity should be shown.
    
    reveal : `bool`
        Whether the response should be revealed.
    
    Returns
    -------
    flags : `int`
    """
    flags = 0
    
    if reveal:
        flags |= FEATURE_FLAG_REVEALED
    
    if detailed:
        flags |= FEATURE_FLAG_DETAILED
    
    channel = interaction_event.channel
    if (channel.type is ChannelType.private) and channel.users:
        # If the client is not in the channel, `.users` should be empty.
        flags |= FEATURE_FLAG_DM
    
    return flags


def _get_first_entity_and_choices_processed(choices):
    """
    Gets the first entity of the given choices and applies postprocessing to them as well.
    
    Parameters
    ----------
    choices : ``list<Emoji | Sticker | SoundboardSound>``
        Choices to process.
    
    Returns
    -------
    entity_and_choices : ``(None | Emoji | Sticker | SoundboardSound, None | list<Emoji | Sticker | SoundboardSound>)``
    """
    choices_count = len(choices)
    if choices_count == 0:
        entity = None
    else:
        entity = choices[0]
    
    if choices_count < 2:
        choices = None
    else:
        del choices[25:]
    
    return entity, choices


def get_entity_and_choices_of_message(message):
    """
    Parses all the choices from the given message.
    
    Parameters
    ----------
    message : ``Message``
        The received message.
    
    Returns
    -------
    entity_and_choices : ``(None | Emoji | Sticker | SoundboardSound, None | list<Emoji | Sticker | SoundboardSound>)``
    """
    snapshot = message.snapshot
    if (snapshot is None):
        content = message.content
        stickers = message.stickers
        soundboard_sounds = message.soundboard_sounds
    else:
        content = snapshot.content
        stickers = snapshot.stickers
        soundboard_sounds = message.soundboard_sounds
    
    choices = []
    
    if (soundboard_sounds is not None):
        choices.extend(soundboard_sounds)
    
    if (stickers is not None):
        choices.extend(stickers)
    
    emojis_added = set()
    
    for emoji in parse_custom_emojis_ordered(content):
        if emoji in emojis_added:
            continue
        
        choices.append(emoji)
        emojis_added.add(emoji)
    
    reactions = message.reactions
    if (reactions is not None):
        for reaction in reactions.iter_reactions():
            emoji = reaction.emoji
            if not emoji.is_custom_emoji():
                continue
            
            if emoji in emojis_added:
                continue
            
            choices.append(emoji)
            emojis_added.add(emoji)
    
    return _get_first_entity_and_choices_processed(choices)


def get_entity_and_choices_of_emoji_name(interaction_event, emoji_name):
    """
    Tries to resolve emojis from a raw version.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    emoji_name : `str`
        The emoji's name.
    
    Returns
    -------
    entity_and_choices : ``(None | Emoji, None | list<Emoji>)``
    """
    while True:
        emoji = parse_emoji(emoji_name)
        if (emoji is not None):
            entity = emoji
            choices = None
            break
        
        # Try resolve emoji from guild's.
        guild = interaction_event.guild
        if (guild is not None):
            emojis = guild.get_emojis_like(emoji_name)
            if emojis:
                entity, choices = _get_first_entity_and_choices_processed(emojis)
                break
        
        entity = None
        choices = None
        break
    
    return entity, choices


async def get_entity_and_choices_of_sticker_name_or_id(interaction_event, sticker_name_or_id):
    """
    Tries to resolve stickers from a raw version.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    sticker_name_or_id : `str`
        The sticker's name or its identifier.
    
    Returns
    -------
    entity_and_choices : ``(None | Sticker, None | list<Sticker>)``
    """
    while True:
        if is_id(sticker_name_or_id):
            sticker = await get_sticker(int(sticker_name_or_id))
            if (sticker is not None):
                entity = sticker
                choices = None
                break
            
            entity = None
            choices = None
            break
        
        guild = interaction_event.guild
        if (guild is not None):
            stickers = guild.get_stickers_like(sticker_name_or_id)
            if stickers:
                entity, choices = _get_first_entity_and_choices_processed(stickers)
                break
        
        entity = None
        choices = None
        break
    
    return entity, choices


async def get_entity_and_choices_of_soundboard_sound_name(interaction_event, soundboard_sound_name):
    """
    Tres to resolve the sound by its name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    soundboard_sound_name : `str`
        The sound's name.
    
    Returns
    -------
    entity_and_choices : ``(None | SoundboardSound, None | list<SoundboardSound>)``
    """
    while True:
        guild = interaction_event.guild
        if (guild is None):
            entity = None
            choices = None
            break
        
        await request_soundboard_sounds_of(guild)
        
        soundboard_sounds = guild.get_soundboard_sounds_like(soundboard_sound_name)
        if soundboard_sounds:
            entity, choices = _get_first_entity_and_choices_processed(soundboard_sounds)
            break
        
        entity = None
        choices = None
        break
    
    return entity, choices


async def get_autocomplete_suggestions_for_emoji_name(interaction_event, emoji_name):
    """
    Gets auto-complete suggestion for the given emoji's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    emoji_name : `None`, `str`
        The typed value.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    if emoji_name is None:
        guild = interaction_event.guild
        if guild is None:
            return
        
        return sorted(emoji.name for emoji in islice(guild.emojis.values(), 0, 25))
    
    emoji = parse_emoji(emoji_name)
    if emoji is not None:
        if not emoji.is_custom_emoji():
            return
        
        return [emoji.as_emoji]
        
    guild = interaction_event.guild
    if guild is None:
        return
    
    return [emoji.name for emoji in guild.get_emojis_like(emoji_name)]


async def get_autocomplete_suggestions_for_sticker_name_or_id(interaction_event, sticker_name_or_id):
    """
    Gets auto-complete suggestion for the given sticker's name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    sticker_name_or_id : `None`, `str`
        The typed value.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    if (sticker_name_or_id is not None) and is_id(sticker_name_or_id):
        return [sticker_name_or_id]
        
    guild = interaction_event.guild
    if guild is None:
        return None
    
    if sticker_name_or_id is None:
        return sorted(sticker.name for sticker in guild.stickers.values())
    
    return [sticker.name for sticker in guild.get_stickers_like(sticker_name_or_id)]


async def get_autocomplete_suggestions_for_soundboard_sound_name(interaction_event, soundboard_sound_name):
    """
    Tries to autocomplete the soundboard sound by its name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    soundboard_sound_name : `None | str`
        The typed value.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    guild = interaction_event.guild
    if guild is None:
        return None
    
    await request_soundboard_sounds_of(guild)
    
    if soundboard_sound_name is None:
        return sorted(soundboard_sound.name for soundboard_sound in guild.iter_soundboard_sounds())
    
    return [soundboard_sound.name for soundboard_sound in guild.get_soundboard_sounds_like(soundboard_sound_name)]


def parse_choices(interaction_event, user_id, feature_flags):
    """
    Parses back the choices of the given interaction event.
    
    Parameters
    ----------
    interaction_event : ``InteractionEvent``
        The received interaction event.
    
    user_id : `int`
        The original invoking user's identifier as hexadecimal integer.
    
    feature_flags : `int`
        The current feature flags of the snipe as hexadecimal string.
    
    Returns
    -------
    choices : ``None | list<Emoji, Sticker, SoundboardSound>``
    """
    choices = None
    choice_select_custom_id = CUSTOM_ID_SNIPE_CHOICE_BUILDER(user_id, feature_flags)
    
    for component in interaction_event.message.iter_components():
        if component.type is not ComponentType.row:
            continue
        
        for component in component.iter_components():
            if (component.type is not ComponentType.string_select) or (component.custom_id != choice_select_custom_id):
                continue
            
            for option in component.iter_options():
                choice = unpack_entity(option.value)
                if (choice is None):
                    continue
                
                if choices is None:
                    choices = []
                
                choices.append(choice)
                continue
            
            break
        
        else:
            continue
        
        break
    
    return choices


def identify_input_emoji(guild, input_emoji):
    """
    Identify the given input as an emoji.
    
    Parameters
    ----------
    guild : ``Guild``
        The guild to execute the identification for.
    
    input_emoji : `None | str`
        The inputted value.
    
    Returns
    -------
    identified_and_emoji : ``(bool, None | Emoji)``
    """
    identified = True
    
    while True:
        if (input_emoji is None):
            emoji = None
            break
        
        emoji = parse_emoji(input_emoji)
        if (emoji is not None):
            break
        
        try:
            emoji_id = int(input_emoji)
        except ValueError:
            pass
        else:
            try:
                emoji = guild.emojis[emoji_id]
            except KeyError:
                pass
            else:
                break
        
        try:
            emoji = UNICODE_TO_EMOJI[input_emoji]
        except KeyError:
            pass
        else:
            break
        
        emoji = guild.get_emoji(input_emoji)
        if (emoji is not None):
            break
        
        try:
            emoji = BUILTIN_EMOJIS[input_emoji]
        except KeyError:
            pass
        else:
            break
        
        emoji = guild.get_emoji_like(input_emoji)
        if (emoji is not None):
            break
        
        # No other cases
        identified = False
        emoji = None
        break
    
    return identified, emoji


def identify_input_tags(input_tags):
    """
    Identifies the passed tags.
    
    Parameters
    ----------
    input_tags : `str`
        Tags to identify.
    
    Returns
    -------
    identifier_and_tags : `(bool, None | tuple<str>)`
    """
    while True:
        if input_tags is None:
            tags = None
            break
        
        tags = set()
        
        for tag in input_tags.split(','):
            tag = tag.strip()
            if tag:
                tags.add(tag)
    
        if not tags:
            tags = None
            break
        
        tags = tuple(sorted(tags))
        break
    
    return True, tags


def identify_input_role_ids(input_roles):
    """
    Identifies the identifiers of the given roles.
    
    Parameters
    ----------
    input_roles : ``None | tuple<Role>``
        Roles to identify.
    
    Returns
    -------
    identified_and_role_ids : `(bool, None | tuple<str>)`
    """
    while True:
        if input_roles is None:
            role_ids = None
            break
        
        role_ids = tuple(sorted(role.id for role in input_roles))
        break
    
    return True, role_ids
