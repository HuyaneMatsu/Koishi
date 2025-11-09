__all__ = ()

from hata import (
    DATETIME_FORMAT_CODE, Emoji, ROLES, SoundboardSound, Sticker, StickerFormat, StickerType, ZEROUSER, elapsed_time
)


FORM_ROLES_DESCRIPTION_MIDDLE = (
    'Limits the Emoji\'s usage only to users with any of the specified roles, current guild only.'
)


def _produce_string(name, value):
    """
    Produces a single string.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Section name to use.
    
    value :`str`
        Value to produce.
    
    Yields
    ------
    part : `str`
    """
    yield name
    yield ': '
    yield value


def _produce_boolean(name, value):
    """
    Produces a single boolean.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Section name to use.
    
    value :`bool`
        Value to produce.
    
    Yields
    ------
    part : `str`
    """
    yield name
    yield ': '
    yield ('true' if value else 'false')


def _produce_user(name, user, guild_id):
    """
    Produces a single user.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Section name to use.
    
    user :``ClientUserBase``
        Value to produce.
    
    guild_id : `int`
        The local guild's identifier.
    
    Yields
    ------
    part : `str`
    """
    yield name
    yield ': '
    
    if user is ZEROUSER:
        yield 'unknown'
    else:
        yield user.name_at(guild_id)
        yield ' | '
        yield str(user.id) 


def _produce_guild(name, guild):
    """
    Produces a single guild.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Section name to use.
    
    guild : ``None | Guild``
        Value to produce.
    
    Yields
    ------
    part : `str`
    """
    yield name
    yield ': '
    
    if guild is None:
        yield 'unknown'
    else:
        yield guild.name
        yield ' | '
        yield str(guild.id)


def _produce_date_time_ago(name, date_time):
    """
    Produces a single date time with ago postfix.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    name : `str`
        Section name to use.
    
    date_time : ``DateTime``
        Value to produce.
    
    Yields
    ------
    part : `str`
    """
    yield name
    yield ': '
    yield format(date_time, DATETIME_FORMAT_CODE)
    yield ' | '
    yield elapsed_time(date_time)
    yield ' ago'


def _produce_description_extend_emoji(emoji, guild_id):
    """
    Produces description extend for emoji.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    emoji : ``Emoji``
        Emoji to produce description of.
    
    guild_id : `int`
        The identifier of the local guild.
    
    Yields
    ------
    part : `str`
    """
    if emoji.is_unicode_emoji():
        yield from _produce_string('\nUnicode', emoji.unicode)
        return
    
    elif emoji.is_custom_emoji():
        yield from _produce_boolean('\nAnimated', emoji.animated)
        yield from _produce_boolean('\nAvailable', emoji.available)
        yield from _produce_boolean('\nManaged', emoji.managed)
        yield from _produce_date_time_ago('\nCreated at', emoji.created_at)
        yield from _produce_user('\nCreator', emoji.user, guild_id)
        yield from _produce_guild('\nGuild', emoji.guild)
        
        yield '\nRoles: '
        role_ids = emoji.role_ids
        if (role_ids is None):
            yield '*none*'
        else:
            role_count = len(role_ids)
            if role_count > 25:
                truncated_count = role_count - 25
                role_count = 25
            else:
                truncated_count = 0
            
            for index in range(role_count):
                if index:
                    yield ', '
                
                try:
                    role = ROLES[role_ids[index]]
                except KeyError:
                    yield '@'
                    yield '\u200b'
                    yield 'deleted role'
                    continue
                
                if guild_id and (emoji.guild_id == guild_id):
                    yield role.mention
                    continue
                
                yield '@'
                yield '\u200b'
                yield role.name
                continue
                    
            if truncated_count:
                yield ', +'
                yield str(truncated_count)
                yield ' truncated...'


def _produce_description_extend_sticker(sticker, guild_id):
    """
    Produces description extend for sticker.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    sticker : ``Sticker``
        Sticker to produce description of.
    
    guild_id : `int`
        The identifier of the local guild.
    
    Yields
    ------
    part : `str`
    """
    sticker_format = sticker.format
    if sticker_format is StickerFormat.apng:
        animated = True
    elif sticker_format is StickerFormat.lottie:
        animated = True
    else:
        animated = False
    
    yield from _produce_boolean('\nAnimated', animated)
    yield from _produce_boolean('\nAvailable', sticker.available)
    yield from _produce_date_time_ago('\nCreated at', sticker.created_at)
    
    yield '\nDescription: '
    description = sticker.description
    yield ('*none*' if description is None else description)
    
    yield '\n'
    sticker_type = sticker.type
    yield from _produce_string('Type', sticker_type.name)
    yield '\n'
    yield from _produce_string('Format', sticker_format.name)
    
    yield '\nTags: '
    tags = sticker.tags
    if tags is None:
        yield '*none*'
    
    else:
        tags = sorted(tags)
        for index in range(len(tags)):
            if index:
                yield ', '
            yield tags[index]
    
    if sticker_type is StickerType.standard:
        yield from _produce_string('\nPack id', str(sticker.pack_id))
        yield from _produce_string('\nSort value', str(sticker.sort_value))
    
    elif sticker_type is StickerType.guild:
        yield from _produce_user('\nCreator', sticker.user, guild_id)
        yield from _produce_guild('\nGuild', sticker.guild)


def _produce_description_extend_soundboard_sound(soundboard_sound, guild_id):
    """
    Produces description extend for soundboard sound.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    soundboard_sound : ``SoundboardSound``
        Soundboard sound to produce description of.
    
    guild_id : `int`
        The identifier of the local guild.
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_date_time_ago('\nCreated at', soundboard_sound.created_at)
    yield from _produce_string('\nVolume', format(soundboard_sound.volume, '.02f'))
    
    yield '\nEmoji: '
    emoji = soundboard_sound.emoji
    yield ('*none' if emoji is None else emoji.name)
    
    if soundboard_sound.is_custom_sound():
        type_name = 'custom'
    elif soundboard_sound.is_default_sound():
        type_name = 'default'
    else:
        type_name = 'unknown'
    
    yield from _produce_string('\nType', type_name)
    
    if soundboard_sound.is_custom_sound():
        yield from _produce_user('\nCreator', soundboard_sound.user, guild_id)
        yield from _produce_guild('\nGuild', soundboard_sound.guild)


def produce_description(entity, guild_id, produce_long):
    """
    Produces description of the given entity.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    entity : ``Emoji | Sticker | SoundboardSound``
        Entity to produce description of.
    
    guild_id : `int`
        The local guild's identifier.
    
    produce_long : `int`
        Whether to produce long description.
    
    Yields
    ------
    part : `str`
    """
    yield from _produce_string('Name', entity.name)
    yield from _produce_string('\nIdentifier', str(entity.id))
    
    if not produce_long:
        return
    
    entity_type = type(entity)
    if entity_type is Emoji:
        yield from _produce_description_extend_emoji(entity, guild_id)
    elif entity_type is Sticker:
        yield from _produce_description_extend_sticker(entity, guild_id)
    elif entity_type is SoundboardSound:
        yield from _produce_description_extend_soundboard_sound(entity, guild_id)


def produce_form_roles_component_long_description(role_ids):
    """
    Produces long description for form roles.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    role_ids : `None |tuple<int>`
        Role identifiers to render.
    
    Yields
    ------
    part : `str`
    """
    yield '###Roles\n'
    yield FORM_ROLES_DESCRIPTION_MIDDLE
    yield '\n```\n'
    
    if (role_ids is None):
        yield '*none*'
    
    else:
        role_count = len(role_ids)
        if role_count > 25:
            truncated_count = role_count - 25
            role_count = 25
        else:
            truncated_count = 0
        
        for index in range(role_count):
            if index:
                yield ', '
            
            try:
                role = ROLES[role_ids[index]]
            except KeyError:
                role_name = 'deleted role'
            else:
                role_name = role.name
            
            yield '@'
            yield '\u200b'
            yield role_name
            continue
                
        if truncated_count:
            yield ', +'
            yield str(truncated_count)
            yield ' truncated...'
    
    yield '\n```'


def get_entity_type_name(entity_type):
    """
    Gets the entity type's name.
    
    Parameters
    ----------
    entity_type : ``type<Emoji | Sticker | SoundboardSound>``
        The type of the entity.
    
    Returns
    -------
    entity_type_name : `str`
    """
    if entity_type is Emoji:
        entity_type_name = 'emoji'
    elif entity_type is Sticker:
        entity_type_name = 'sticker'
    elif entity_type is SoundboardSound:
        entity_type_name = 'sound'
    else:
        entity_type_name = 'unknown'
    
    return entity_type_name
