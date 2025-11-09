__all__ = ()

from base64 import b64decode as base_64_decode, b64encode as base_64_encode

from hata import Emoji, SoundboardSound, Sticker

from .constants import (
    CHOICE_TYPE_IDENTIFIER_EMOJI, CHOICE_TYPE_IDENTIFIER_NONE, CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND,
    CHOICE_TYPE_IDENTIFIER_STICKER
)


def pack_entity(entity):
    """
    Packs the entity.
    
    Parameters
    ----------
    entity : ``Emoji | Sticker | SoundboardSound``
        The entity to pack.
    
    Returns
    -------
    value : `str`
    """
    entity_type = type(entity)
    if entity_type is Emoji:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_EMOJI
        entity_guild_id = entity.guild_id
        entity_id = entity.id
        entity_animated = entity.animated
        entity_name = entity.name
    
    elif entity_type is Sticker:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_STICKER
        entity_guild_id = entity.guild_id
        entity_id = entity.id
        entity_animated = False
        entity_name = entity.name
        
    elif entity_type is SoundboardSound:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND
        entity_guild_id = entity.guild_id
        entity_id = entity.id
        entity_animated = False
        entity_name = entity.name
        
    else:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_NONE
        entity_guild_id = 0
        entity_id = 0
        entity_animated = False
        entity_name = ''
    
    return base_64_encode(b''.join([
        entity_type_id.to_bytes(1, 'little'),
        entity_guild_id.to_bytes(8, 'little'),
        entity_id.to_bytes(8, 'little'),
        entity_animated.to_bytes(1, 'little'),
        entity_name.encode(),
    ])).decode()


def pack_entity_type(entity_type):
    """
    Packs just the given entity type.
    
    Parameters
    ----------
    entity_type : ``type<Emoji | Sticker | SoundboardSound>``
        The type to pack.
    
    Returns
    -------
    value : `str`
    """
    if entity_type is Emoji:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_EMOJI
    
    elif entity_type is Sticker:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_STICKER
        
    elif entity_type is SoundboardSound:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND
        
    else:
        entity_type_id = CHOICE_TYPE_IDENTIFIER_NONE
    
    return format(entity_type_id, 'x')


def unpack_entity(value):
    """
    Unpacks an entity from the given value.
    
    Parameters
    ----------
    value : `str`
        Value to unpack.
    
    Returns
    -------
    entity : ``None | Emoji | Sticker | SoundboardSound``
    """
    try:
        binary = base_64_decode(value)
    except ValueError:
        return None
    
    if len(binary) < 18:
        return None
    
    try:
        entity_type_id = int.from_bytes(binary[0 : 1], 'little')
        entity_guild_id = int.from_bytes(binary[1 : 9], 'little')
        entity_id = int.from_bytes(binary[9 : 17], 'little')
        entity_animated = True if int.from_bytes(binary[17 : 18], 'little') else False
        entity_name = binary[18: ].decode()
    except ValueError:
        return None
    
    if entity_type_id == CHOICE_TYPE_IDENTIFIER_NONE:
        entity = None
    
    elif entity_type_id == CHOICE_TYPE_IDENTIFIER_EMOJI:
        entity = Emoji.precreate(entity_id, animated = entity_animated, guild_id = entity_guild_id, name = entity_name)
    
    elif entity_type_id == CHOICE_TYPE_IDENTIFIER_STICKER:
        entity = Sticker.precreate(entity_id, guild_id = entity_guild_id, name = entity_name)
    
    elif entity_type_id == CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND:
        entity = SoundboardSound.precreate(entity_id, guild_id = entity_guild_id, name = entity_name)
    
    else:
        entity = None
    
    return entity


def unpack_entity_type(value):
    """
    Unpacks an entity type from the given value.
    
    Parameters
    ----------
    value : `str`
        Value to unpack.
    
    Returns
    -------
    entity_type : ``None | type<Emoji | Sticker | SoundboardSound>``
    """
    try:
        entity_type_id = int(value, 16)
    except ValueError:
        return
    
    if entity_type_id == CHOICE_TYPE_IDENTIFIER_NONE:
        entity_type = None
    
    elif entity_type_id == CHOICE_TYPE_IDENTIFIER_EMOJI:
        entity_type = Emoji
    
    elif entity_type_id == CHOICE_TYPE_IDENTIFIER_STICKER:
        entity_type = Sticker
    
    elif entity_type_id == CHOICE_TYPE_IDENTIFIER_SOUNDBOARD_SOUND:
        entity_type = SoundboardSound
    
    else:
        entity_type = None
    
    return entity_type
