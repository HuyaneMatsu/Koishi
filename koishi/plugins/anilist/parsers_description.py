__all__ = ()

from re import M as re_multi_line, S as re_dotall, U as re_unicode, compile as re_compile

from .constants import DESCRIPTION_LENGTH_MAX
from .parsers_date import parse_fuzzy_date
from .keys import (
    KEY_CHARACTER_AGE, KEY_CHARACTER_BIRTH_DATE, KEY_CHARACTER_BLOOD_TYPE, KEY_CHARACTER_DESCRIPTION,
    KEY_CHARACTER_GENDER, KEY_MEDIA_DESCRIPTION, KEY_MEDIA_GENRES, KEY_CHARACTER_MEDIA_CONNECTIONS,
    KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY
)
from .parsers_name import parse_name_media, parse_name_character
from .parsers_url import parse_url_media, parse_url_anime, parse_url_character, parse_url_manga


TO_REMOVE = '\(\d+\'(?:\d+\")?\)'


DESCRIPTION_RP = re_compile(
    (
        f'~!|' # Spoiler tag
        f'!~|' # Spoiler tag ending
        f'__|' # bold
        f' {TO_REMOVE}|{TO_REMOVE} ?|' # US shit
        f'<br/?>(?:<br>)?|' # They don't know what not html format means
        f'&#039|' # They don't know what not html format means
        f'</?(?:i|em)/?>' # They don't know what not html format means
    ),
    re_multi_line | re_unicode | re_dotall,
)

DESCRIPTION_RELATION = {
    '~!': '||',
    '!~': '||',
    '__': '**',
    '<br><br>': '\n',
    '<br>': '\n',
    '<br/>': '\n',
    '&#039': '\'',
    '<i>': '*',
    '</i>': '*',
    '<i/>': '*',
    '<em>': '`',
    '</em>': '`',
    '<em/>': '`',
}


DESCRIPTION_ESCAPER = lambda match: DESCRIPTION_RELATION.get(match.group(0), '')


def escape_description(description):
    """
    Escapes the given description.
    
    Parameters
    ----------
    description : `None`, `str`
        The description to escape.
    
    Returns
    -------
    description : `None`, `str`
    """
    if (description is None) or (not description):
        return None
    
    description = DESCRIPTION_RP.sub(DESCRIPTION_ESCAPER, description)
    if not description:
        return None
    
    return description


def limit_string_length(string, max_length):
    """
    Limits the string's length to the given length.
    
    Parameters
    ----------
    string : `None`, `str`
        String to limit its length of.
    max_length : `int`
        The maximal allowed length. Must be positive.
    
    Returns
    -------
    string : `None`, `str`
    """
    if (string is not None) and (len(string) > max_length):
        string = string[: max_length - 4] + ' ...'
    
    return string


def render_inline_section_into(into, field_added, section_title, section_content):
    """
    Renders an inline section into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    section_title : `str`
        The section's title.
    section_content : `None`, `str`
        The section's content.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (section_content is not None) and section_content:
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append('**')
        into.append(section_title)
        into.append(':** ')
        into.append(section_content)
    
    return into, field_added


def render_inline_listing_section_into(into, field_added, section_title, listing):
    """
    Renders an inline listing section into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    section_title : `str`
        The section's title.
    listing : `null | list<str>`
        The listing to render.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    if (listing is not None) and listing:
        if field_added:
            into.append('\n')
        else:
            field_added = True
        
        into.append('**')
        into.append(section_title)
        into.append(':** ')
        
        index = 0
        limit = len(listing)
        
        while True:
            genre = listing[index]
            index += 1
            
            into.append(genre)
            if index == limit:
                break
            
            into.append(', ')
            continue
        
    return into, field_added


def render_description_into(into, field_added, description):
    """
    Renders description into the given container.
    
    Parameters
    ----------
    into : `list<str>`
        The container to render into.
    field_added : `bool`
        Whether any fields were added already.
    description : `None | str`
        Description to render.
    
    Returns
    -------
    into : `list<str>`
    field_added : `bool`
    """
    description = escape_description(description)
    if (description is not None):
        if field_added:
            if description.startswith('**'):
                into.append('\n')
            elif description.startswith('\n**'):
                pass
            elif description.startswith('\n'):
                into.append('\n')
            else:
                into.append('\n\n')
        
        else:
            field_added = True
        
        into.append(description)
    
    return into, field_added


def parse_description_character(character_data):
    """
    Parses a character's description.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character data to parse the description from.
    
    Returns
    -------
    description : `None`, `str`
    """
    description_parts = []
    field_added = False
    
    description_parts, field_added = render_inline_section_into(
        description_parts, field_added, 'Birthday', parse_fuzzy_date(character_data.get(KEY_CHARACTER_BIRTH_DATE, None))
    )
    
    description_parts, field_added = render_inline_section_into(
        description_parts, field_added, 'Age', character_data.get(KEY_CHARACTER_AGE, None)
    )
    
    description_parts, field_added = render_inline_section_into(
        description_parts, field_added, 'Gender', character_data.get(KEY_CHARACTER_GENDER, None)
    )
    
    description_parts, field_added = render_inline_section_into(
        description_parts, field_added, 'Blood type', character_data.get(KEY_CHARACTER_BLOOD_TYPE, None)
    )
    
    description_parts,field_added = render_description_into(
        description_parts, field_added, character_data.get(KEY_CHARACTER_DESCRIPTION, None)
    )
    
    if field_added:
        description = ''.join(description_parts)
    else:
        description = None
    
    return limit_string_length(description, DESCRIPTION_LENGTH_MAX)


def parse_description_media(media_data):
    """
    Parses a media's description.
    
    Parameters
    ----------
    media_data : `dict<str, object>`
        Media data to parse the description from.
    
    Returns
    -------
    description : `None`, `str`
    """
    description_parts = []
    field_added = False
    
    description_parts, field_added = render_inline_listing_section_into(
        description_parts, field_added, 'Genres', media_data.get(KEY_MEDIA_GENRES, None), 
    )
    
    description_parts,field_added = render_description_into(
        description_parts, field_added, media_data.get(KEY_MEDIA_DESCRIPTION, None)
    )
    
    if field_added:
        description = ''.join(description_parts)
    else:
        description = None
    
    return limit_string_length(description, DESCRIPTION_LENGTH_MAX)


def parse_listing_base(array_data, name_parser, url_parser):
    """
    Builds entity listing description.
    
    Parameters
    ----------
    array_data : `None | list<dict<str, object>>`
        Array of entity data.
    name_parser : `FunctionType`
        Name parser to use.
    url_parser : `FunctionType`
        Url parser to use.
    
    Returns
    -------
    entity_listing : `None`, `str`
    """
    if (array_data is None) or (not array_data):
        return
    
    description_parts = []
    
    array_index = 0
    array_limit = len(array_data)
    
    while True:
        entity_data = array_data[array_index]
        array_index += 1
        
        media_name = name_parser(entity_data)
        media_url = url_parser(entity_data)
        
        if media_url is None:
            description_parts.append(media_name)
        else:
            description_parts.append('[')
            description_parts.append(media_name)
            description_parts.append('](')
            description_parts.append(media_url)
            description_parts.append(')')
        
        if array_index == array_limit:
            break
        
        description_parts.append('\n')
        continue
    
    return ''.join(description_parts)


def parse_listing_anime(array_data):
    """
    Builds anime listing description.
    
    Parameters
    ----------
    array_data : `None | list<dict<str, object>>`
        Array of entity data.
    
    Returns
    -------
    entity_listing : `None`, `str`
    """
    return parse_listing_base(array_data, parse_name_media, parse_url_anime)


def parse_listing_character(array_data):
    """
    Builds character listing description.
    
    Parameters
    ----------
    array_data : `None | list<dict<str, object>>`
        Array of entity data.
    
    Returns
    -------
    entity_listing : `None`, `str`
    """
    return parse_listing_base(array_data, parse_name_character, parse_url_character)


def parse_listing_manga(array_data):
    """
    Builds manga listing description.
    
    Parameters
    ----------
    array_data : `None | list<dict<str, object>>`
        Array of entity data.
    
    Returns
    -------
    entity_listing : `None`, `str`
    """
    return parse_listing_base(array_data, parse_name_media, parse_url_manga)


def parse_character_media_connections_description(character_data):
    """
    Parses character media connections description form the given data.
    
    Parameters
    ----------
    character_data : `dict<str, object>`
        Character to parse from.
    
    Returns
    -------
    description : `None`, `str`
    """
    media_connections_data = character_data.get(KEY_CHARACTER_MEDIA_CONNECTIONS, None)
    if media_connections_data is None:
        return
    
    media_connections_array_data = media_connections_data.get(KEY_CHARACTER_MEDIA_CONNECTIONS_MEDIA_ARRAY, None)
    return parse_listing_base(media_connections_array_data, parse_name_media, parse_url_media)
