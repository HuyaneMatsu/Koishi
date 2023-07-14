import vampytest
from hata.discord.component.component_metadata.constants import LABEL_LENGTH_MAX
from hata.ext.slash import Option

from ..keys import KEY_CHARACTER_ID, KEY_CHARACTER_NAME, KEY_MEDIA_ID, KEY_MEDIA_NAME, \
    KEY_CHARACTER_NAME_FIRST, KEY_MEDIA_NAME_ROMAJI
from ..parsers_components import parse_option_character, parse_option_media, parse_option_base
from ..parsers_name import NAME_DEFAULT, parse_name_character, parse_name_media


def _iter_options__parse_option_base():
    yield (
        {},
        KEY_CHARACTER_ID,
        parse_name_character,
        Option('-1', NAME_DEFAULT),
    )
    
    yield (
        {
            KEY_CHARACTER_NAME: {
                KEY_CHARACTER_NAME_FIRST: 'koishi',
            },
            KEY_CHARACTER_ID: 56,
        },
        KEY_CHARACTER_ID,
        parse_name_character,
        Option(
            str(56),
            'koishi',
        )
    )

    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'koishi',
            },
            KEY_MEDIA_ID: 56,
        },
        KEY_MEDIA_ID,
        parse_name_media,
        Option(
            str(56),
            'koishi',
        )
    )


@vampytest._(vampytest.call_from(_iter_options__parse_option_base()).returning_last())
def test__parse_option_base(entity_data, key_id, name_parser):
    """
    Tests whether ``parse_option_base`` works as intended.
    
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
    return parse_option_base(entity_data, key_id, name_parser)


def _iter_options__parse_option_character():
    yield (
        {},
        Option('-1', NAME_DEFAULT),
    )
    
    yield (
        {
            KEY_CHARACTER_NAME: {
                KEY_CHARACTER_NAME_FIRST: 'koishi',
            },
            KEY_CHARACTER_ID: 56,
        },
        Option(
            str(56),
            'koishi',
        )
    )
    
    yield (
        {
            KEY_CHARACTER_NAME: {
                KEY_CHARACTER_NAME_FIRST: 'a' * (LABEL_LENGTH_MAX + 1),
            },
        },
        Option(
            '-1',
            'a' * (LABEL_LENGTH_MAX - 4) + ' ...',
        )
    )


@vampytest._(vampytest.call_from(_iter_options__parse_option_character()).returning_last())
def test__parse_option_character(entity_data):
    """
    Tests whether ``parse_option_character`` works as intended.
    
    Parameters
    ----------
    entity_data : `dict<str, object>`
        Entity data.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return parse_option_character(entity_data)


def _iter_options__parse_option_media():
    yield (
        {},
        Option('-1', NAME_DEFAULT),
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'koishi',
            },
            KEY_MEDIA_ID: 56,
        },
        Option(
            str(56),
            'koishi',
        )
    )
    
    yield (
        {
            KEY_MEDIA_NAME: {
                KEY_MEDIA_NAME_ROMAJI: 'a' * (LABEL_LENGTH_MAX + 1),
            },
        },
        Option(
            '-1',
            'a' * (LABEL_LENGTH_MAX - 4) + ' ...',
        )
    )


@vampytest._(vampytest.call_from(_iter_options__parse_option_media()).returning_last())
def test__parse_option_media(entity_data):
    """
    Tests whether ``parse_option_media`` works as intended.
    
    Parameters
    ----------
    entity_data : `dict<str, object>`
        Entity data.
    
    Returns
    -------
    option : ``StringSelectOption``
    """
    return parse_option_media(entity_data)
