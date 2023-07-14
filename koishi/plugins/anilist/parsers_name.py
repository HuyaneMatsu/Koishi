__all__ = ()

from .keys import (
    KEY_CHARACTER_NAME, KEY_CHARACTER_NAME_FIRST, KEY_CHARACTER_NAME_LAST, KEY_CHARACTER_NAME_MIDDLE,
    KEY_CHARACTER_NAME_NATIVE, KEY_MEDIA_NAME, KEY_MEDIA_NAME_NATIVE, KEY_MEDIA_NAME_ROMAJI
)

NAME_DEFAULT = '???'


def parse_name_character(character_data):
    """
    Parses the name of the character from the given data.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        The character data.
    
    Returns
    -------
    character_name : `str`
    """
    name_data = character_data.get(KEY_CHARACTER_NAME, None)
    if name_data is None:
        return NAME_DEFAULT
    
    name_first = name_data.get(KEY_CHARACTER_NAME_FIRST, None)
    name_middle = name_data.get(KEY_CHARACTER_NAME_MIDDLE, None)
    name_last = name_data.get(KEY_CHARACTER_NAME_LAST, None)
    name_native = name_data.get(KEY_CHARACTER_NAME_NATIVE, None)
    
    name_parts = []
    
    if (name_first is not None):
        name_parts.append(name_first)
        
        field_added = True
    else:
        field_added = False
    
    if (name_middle is not None):
        if field_added:
            name_parts.append(' ')
        else:
            field_added = True
        
        name_parts.append(name_middle)
    
    if (name_last is not None):
        if field_added:
            name_parts.append(' ')
        else:
            field_added = True
        
        name_parts.append(name_last)
    
    if (name_native is not None):
        if field_added:
            name_parts.append(' (')
        
        name_parts.append(name_native)
        
        if field_added:
            name_parts.append(')')
        else:
            field_added = True
    
    if not field_added:
        return NAME_DEFAULT
    
    return ''.join(name_parts)


def parse_name_media(media_data):
    """
    Parses the name of the media from the given data.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        The media data.
    
    Returns
    -------
    media_name : `str`
    """
    name_data = media_data.get(KEY_MEDIA_NAME, None)
    if name_data is None:
        return NAME_DEFAULT
    
    name_romaji = name_data.get(KEY_MEDIA_NAME_ROMAJI, None)
    name_native = name_data.get(KEY_MEDIA_NAME_NATIVE, None)
    
    if (name_romaji is None):
        if (name_native is None):
            name = NAME_DEFAULT
        else:
            name = name_native
    else:
        if (name_native is None) or (name_romaji == name_native):
            name = name_romaji
        else:
            name = f'{name_romaji} ({name_native})'
    
    return name
