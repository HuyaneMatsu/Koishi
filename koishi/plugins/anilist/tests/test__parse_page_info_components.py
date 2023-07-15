import vampytest
from hata.ext.slash import Button, Row

from ..constants import (
    COMPONENT_LEFT_ANIME, COMPONENT_LEFT_CHARACTER, COMPONENT_LEFT_DISABLED, COMPONENT_LEFT_MANGA,
    COMPONENT_RIGHT_ANIME, COMPONENT_RIGHT_CHARACTER, COMPONENT_RIGHT_DISABLED, COMPONENT_RIGHT_MANGA
)
from ..keys import KEY_PAGE_INFO_CURRENT, KEY_PAGE_INFO_TOTAL
from ..parsers_components import (
    parse_page_info_components_anime, parse_page_info_components_base, parse_page_info_components_character,
    parse_page_info_components_manga
)


def _iter_options__parse_page_info_components_base():
    component_0 = Button('koishi')
    component_1 = Button('satori')
    
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        component_0,
        component_1,
        Row(component_0, component_1),
    )
    
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 2,
        },
        component_0,
        component_1,
        Row(component_0, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        component_0,
        component_1,
        Row(COMPONENT_LEFT_DISABLED, component_1),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 1,
        },
        component_0,
        component_1,
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {},
        component_0,
        component_1,
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_page_info_components_base()).returning_last())
def test__parse_page_info_components_base(page_info_data, button_left, button_right):
    """
    Tests whether ``parse_page_info_components_base`` works as intended.
    
    Parameters
    ----------
    page_info_data : `int`
        Page info data.
    button_left : ``Component``
        Left component to use.
    button_right : ``Component``
        Right component to use.
    
    Returns
    -------
    component : ``Component``
    """
    return parse_page_info_components_base(page_info_data, button_left, button_right)


def _iter_options__parse_page_info_components_character():
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        Row(COMPONENT_LEFT_CHARACTER, COMPONENT_RIGHT_CHARACTER),
    )
    
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 2,
        },
        Row(COMPONENT_LEFT_CHARACTER, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_CHARACTER),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 1,
        },
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {},
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_page_info_components_character()).returning_last())
def test__parse_page_info_components_character(page_info_data):
    """
    Tests whether ``parse_page_info_components_character`` works as intended.
    
    Parameters
    ----------
    page_info_data : `int`
        Page info data.
    
    Returns
    -------
    component : ``Component``
    """
    return parse_page_info_components_character(page_info_data)


def _iter_options__parse_page_info_components_anime():
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        Row(COMPONENT_LEFT_ANIME, COMPONENT_RIGHT_ANIME),
    )
    
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 2,
        },
        Row(COMPONENT_LEFT_ANIME, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_ANIME),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 1,
        },
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {},
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_page_info_components_anime()).returning_last())
def test__parse_page_info_components_anime(page_info_data):
    """
    Tests whether ``parse_page_info_components_anime`` works as intended.
    
    Parameters
    ----------
    page_info_data : `int`
        Page info data.
    
    Returns
    -------
    component : ``Component``
    """
    return parse_page_info_components_anime(page_info_data)


def _iter_options__parse_page_info_components_manga():
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        Row(COMPONENT_LEFT_MANGA, COMPONENT_RIGHT_MANGA),
    )
    
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 2,
        },
        Row(COMPONENT_LEFT_MANGA, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_MANGA),
    )

    yield (
        {
            KEY_PAGE_INFO_CURRENT: 1,
            KEY_PAGE_INFO_TOTAL: 1,
        },
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )

    yield (
        {},
        Row(COMPONENT_LEFT_DISABLED, COMPONENT_RIGHT_DISABLED),
    )


@vampytest._(vampytest.call_from(_iter_options__parse_page_info_components_manga()).returning_last())
def test__parse_page_info_components_manga(page_info_data):
    """
    Tests whether ``parse_page_info_components_manga`` works as intended.
    
    Parameters
    ----------
    page_info_data : `int`
        Page info data.
    
    Returns
    -------
    component : ``Component``
    """
    return parse_page_info_components_manga(page_info_data)
