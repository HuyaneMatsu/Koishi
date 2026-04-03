__all__ = ()

from .keys import KEY_PAGE_INFO_CURRENT, KEY_PAGE_INFO_ENTRIES, KEY_PAGE_INFO_TOTAL


def parse_page_info(page_info_data):
    """
    Parses page info footer text.
    
    Returns
    -------
    page_info_data : `dict<str, object>`
        Page info data.
    
    Returns
    -------
    footer_text : `str`
    """
    page_total = page_info_data.get(KEY_PAGE_INFO_TOTAL, 1)
    page_current = page_info_data.get(KEY_PAGE_INFO_CURRENT, 1)
    text_parts = ['Page: ', str(page_current), ' / ', str(page_total)]
    
    entries = page_info_data.get(KEY_PAGE_INFO_ENTRIES, None)
    if entries is not None:
        text_parts.append(' (')
        text_parts.append(str(entries))
        text_parts.append(' results)')
    
    return ''.join(text_parts)
