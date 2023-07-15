__all__ = ()

from hata.discord.component.component_metadata.constants import LABEL_LENGTH_MAX
from hata.ext.slash import Option, Row

from .constants import (
    COMPONENT_LEFT_ANIME, COMPONENT_LEFT_CHARACTER, COMPONENT_LEFT_DISABLED, COMPONENT_LEFT_MANGA,
    COMPONENT_RIGHT_ANIME, COMPONENT_RIGHT_CHARACTER, COMPONENT_RIGHT_DISABLED, COMPONENT_RIGHT_MANGA,
    COMPONENT_SELECT_ANIME, COMPONENT_SELECT_CHARACTER, COMPONENT_SELECT_MANGA
)
from .keys import KEY_CHARACTER_ID, KEY_MEDIA_ID, KEY_PAGE_INFO_CURRENT, KEY_PAGE_INFO_TOTAL
from .parsers_description import limit_string_length
from .parsers_name import parse_name_character, parse_name_media


def parse_option_base(entity_data, key_id, name_parser):
    """
    Base parser for options.
    
    Parameters
    ----------
    entity_data : `dict<str, object>`
        Entity data.
    key_id : `str`
        The key for the entity's identifier.
    name_parser : `FunctionType`
        Name parser.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    entity_id = entity_data.get(key_id, None)
    if entity_id is None:
        entity_id_str = '-1'
    else:
        entity_id_str = str(entity_id)
    
    entity_name = limit_string_length(name_parser(entity_data), LABEL_LENGTH_MAX)
    return Option(entity_id_str, entity_name)


def parse_option_character(entity_data):
    """
    Parses a character option.
    
    Parameters
    ----------
    entity_data : `dict<str, object>`
        Entity data.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return parse_option_base(entity_data, KEY_CHARACTER_ID, parse_name_character)


def parse_option_media(entity_data):
    """
    Parses a media (anime / manga) option.
    
    Parameters
    ----------
    entity_data : `dict<str, object>`
        Entity data.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return parse_option_base(entity_data, KEY_MEDIA_ID, parse_name_media)


def parse_select_base(entity_array_data, select_base, option_parser):
    """
    Parses a select from the given entity array data.
    
    Parameters
    ----------
    entity_array_data : `None | list<dict<str, object>>`
        Data array to parse from.
    select_base : ``Component``
        Base component to copy.
    option_parser : `FunctionType`
        Option parser to parse a single option.
    
    Returns
    -------
    select : ``Component``
    """
    if (entity_array_data is None) or (not entity_array_data):
        return select_base.copy_with(
            options = [Option('-1', 'No result', default = True)],
            enabled = False,
        )
    
    return select_base.copy_with(
        options = [option_parser(entry_data) for entry_data in entity_array_data],
    )


def parse_select_anime(entity_array_data):
    """
    Parses anime select.
    
    Parameters
    ----------
    entity_array_data : `None | list<dict<str, object>>`
        Data array to parse from.
    
    Returns
    -------
    select : ``Component``
    """
    return parse_select_base(entity_array_data, COMPONENT_SELECT_ANIME, parse_option_media)


def parse_select_character(entity_array_data):
    """
    Parses character select.
    
    Parameters
    ----------
    entity_array_data : `None | list<dict<str, object>>`
        Data array to parse from.
    
    Returns
    -------
    select : ``Component``
    """
    return parse_select_base(entity_array_data, COMPONENT_SELECT_CHARACTER, parse_option_character)


def parse_select_manga(entity_array_data):
    """
    Parses manga select.
    
    Parameters
    ----------
    entity_array_data : `None | list<dict<str, object>>`
        Data array to parse from.
    
    Returns
    -------
    select : ``Component``
    """
    return parse_select_base(entity_array_data, COMPONENT_SELECT_MANGA, parse_option_media)


def parse_page_info_components_base(page_info_data, button_left, button_right):
    """
    Parses page info components.
    
    Returns
    -------
    page_info_data : `dict<str, object>`
        Page info data.
    button_left : ``Component``
        Left component to use.
    button_right : ``Component``
        Right component to use.
    
    Returns
    -------
    components : ``Component``
        A component row.
    """
    page_total = page_info_data.get(KEY_PAGE_INFO_TOTAL, 1)
    page_current = page_info_data.get(KEY_PAGE_INFO_CURRENT, 1)

    if page_current <= 1:
        button_left = COMPONENT_LEFT_DISABLED
    
    if page_current >= page_total:
        button_right = COMPONENT_RIGHT_DISABLED
    
    return Row(button_left, button_right)


def parse_page_info_components_anime(page_info_data):
    """
    Parses anime page info components.
    
    Returns
    -------
    page_info_data : `dict<str, object>`
        Page info data.
    
    Returns
    -------
    components : ``Component``
        A component row.
    """
    return parse_page_info_components_base(page_info_data, COMPONENT_LEFT_ANIME, COMPONENT_RIGHT_ANIME)


def parse_page_info_components_character(page_info_data):
    """
    Parses character page info components.
    
    Returns
    -------
    page_info_data : `dict<str, object>`
        Page info data.
    
    Returns
    -------
    components : ``Component``
        A component row.
    """
    return parse_page_info_components_base(page_info_data, COMPONENT_LEFT_CHARACTER, COMPONENT_RIGHT_CHARACTER)


def parse_page_info_components_manga(page_info_data):
    """
    Parses manga page info components.
    
    Returns
    -------
    page_info_data : `dict<str, object>`
        Page info data.
    
    Returns
    -------
    components : ``Component``
        A component row.
    """
    return parse_page_info_components_base(page_info_data, COMPONENT_LEFT_MANGA, COMPONENT_RIGHT_MANGA)
