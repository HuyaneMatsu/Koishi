import vampytest

from ..keys import KEY_PAGE_INFO_CURRENT, KEY_PAGE_INFO_ENTRIES, KEY_PAGE_INFO_TOTAL
from ..parsers_page_info import parse_page_info


def _iter_options():
    yield (
        {},
        'Page: 1 / 1',
    )
    
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 3,
        },
        'Page: 2 / 3',
    )
    
    yield (
        {
            KEY_PAGE_INFO_CURRENT: 2,
            KEY_PAGE_INFO_TOTAL: 3,
            KEY_PAGE_INFO_ENTRIES: 69,
        },
        'Page: 2 / 3 (69 results)',
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__parse_page_info(page_info_data):
    """
    Tests whether ``parse_page_info`` works as intended.
    
    Returns
    -------
    page_info_data : `dict<str, object>`
        Page info data.
    
    Returns
    -------
    footer_text : `str`
    """
    return parse_page_info(page_info_data)
