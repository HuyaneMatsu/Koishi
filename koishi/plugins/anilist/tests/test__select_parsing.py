import vampytest
from hata import StringSelectOption, create_string_select

from ..constants import COMPONENT_SELECT_ANIME, COMPONENT_SELECT_CHARACTER, COMPONENT_SELECT_MANGA
from ..keys import (
    KEY_CHARACTER_ID, KEY_CHARACTER_NAME, KEY_CHARACTER_NAME_FIRST, KEY_MEDIA_ID, KEY_MEDIA_NAME, KEY_MEDIA_NAME_ROMAJI
)
from ..parsers_components import (
    parse_option_character, parse_option_media, parse_select_anime, parse_select_base, parse_select_character,
    parse_select_manga
)


def _iter_options__parse_select_base():
    select_base = create_string_select(
        None,
        'komeiji',
        placeholder = 'koishi',
    )
    
    yield (
        None,
        select_base,
        parse_option_character,
        select_base.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )
    
    yield (
        [],
        select_base,
        parse_option_character,
        select_base.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )

    yield (
        [
            {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'orin',
                },
                KEY_CHARACTER_ID: 56,
            }, {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'okuu',
                },
                KEY_CHARACTER_ID: 69,
            },
        ],
        select_base,
        parse_option_character,
        select_base.copy_with(
            options = [
                StringSelectOption(
                    str(56),
                    'orin',
                ),
                StringSelectOption(
                    str(69),
                    'okuu',
                )
            ],
        ),
    )

    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'orin',
                },
                KEY_MEDIA_ID: 56,
            }, {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'okuu',
                },
                KEY_MEDIA_ID: 69,
            },
        ],
        select_base,
        parse_option_media,
        select_base.copy_with(
            options = [
                StringSelectOption(
                    str(56),
                    'orin',
                ),
                StringSelectOption(
                    str(69),
                    'okuu',
                )
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_select_base()).returning_last())
def test__parse_select_base(entity_array_data, select_base, option_parser):
    """
    Tests whether ``parse_select_base`` works as intended.
    
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
    option : ``StringSelectOption``
    """
    return parse_select_base(entity_array_data, select_base, option_parser)


def _iter_options__parse_select_character():
    yield (
        None,
        COMPONENT_SELECT_CHARACTER.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )
    
    yield (
        [],
        COMPONENT_SELECT_CHARACTER.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )

    yield (
        [
            {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'orin',
                },
                KEY_CHARACTER_ID: 56,
            }, {
                KEY_CHARACTER_NAME: {
                    KEY_CHARACTER_NAME_FIRST: 'okuu',
                },
                KEY_CHARACTER_ID: 69,
            },
        ],
        COMPONENT_SELECT_CHARACTER.copy_with(
            options = [
                StringSelectOption(
                    str(56),
                    'orin',
                ),
                StringSelectOption(
                    str(69),
                    'okuu',
                )
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_select_character()).returning_last())
def test__parse_select_character(entity_array_data):
    """
    Tests whether ``parse_select_character`` works as intended.
    
    Parameters
    ----------
    entity_array_data : `None | list<dict<str, object>>`
        Data array to parse from.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return parse_select_character(entity_array_data)


def _iter_options__parse_select_anime():
    yield (
        None,
        COMPONENT_SELECT_ANIME.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )
    
    yield (
        [],
        COMPONENT_SELECT_ANIME.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )

    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'orin',
                },
                KEY_MEDIA_ID: 56,
            }, {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'okuu',
                },
                KEY_MEDIA_ID: 69,
            },
        ],
        COMPONENT_SELECT_ANIME.copy_with(
            options = [
                StringSelectOption(
                    str(56),
                    'orin',
                ),
                StringSelectOption(
                    str(69),
                    'okuu',
                )
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_select_anime()).returning_last())
def test__parse_select_anime(entity_array_data):
    """
    Tests whether ``parse_select_anime`` works as intended.
    
    Parameters
    ----------
    entity_array_data : `None | list<dict<str, object>>`
        Data array to parse from.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return parse_select_anime(entity_array_data)


def _iter_options__parse_select_manga():
    yield (
        None,
        COMPONENT_SELECT_MANGA.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )
    
    yield (
        [],
        COMPONENT_SELECT_MANGA.copy_with(
            options = [StringSelectOption('-1', 'No result', default = True)],
            enabled = False,
        ),
    )

    yield (
        [
            {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'orin',
                },
                KEY_MEDIA_ID: 56,
            }, {
                KEY_MEDIA_NAME: {
                    KEY_MEDIA_NAME_ROMAJI: 'okuu',
                },
                KEY_MEDIA_ID: 69,
            },
        ],
        COMPONENT_SELECT_MANGA.copy_with(
            options = [
                StringSelectOption(
                    str(56),
                    'orin',
                ),
                StringSelectOption(
                    str(69),
                    'okuu',
                )
            ],
        ),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_select_manga()).returning_last())
def test__parse_select_manga(entity_array_data):
    """
    Tests whether ``parse_select_manga`` works as intended.
    
    Parameters
    ----------
    entity_array_data : `None | list<dict<str, object>>`
        Data array to parse from.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return parse_select_manga(entity_array_data)
