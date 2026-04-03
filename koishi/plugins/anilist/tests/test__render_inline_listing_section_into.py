import vampytest

from ..parsers_description import render_inline_listing_section_into


def _iter_options():
    yield False, 'Koishi', None, ('', False)
    yield False, 'Koishi', [], ('', False)
    yield False, 'Koishi', ['Satori'], ('**Koishi:** Satori', True)
    yield False, 'Koishi', ['Satori', 'Okuu'], ('**Koishi:** Satori, Okuu', True)
    
    yield True, 'Koishi', None, ('', True)
    yield True, 'Koishi', [], ('', True)
    yield True, 'Koishi', ['Satori'], ('\n**Koishi:** Satori', True)
    yield True, 'Koishi', ['Satori', 'Okuu'], ('\n**Koishi:** Satori, Okuu', True)


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__render_inline_listing_section_into(field_added, section_title, listing):
    """
    Tests whether ``render_inline_listing_section_into`` works as intended.
    
    Parameters
    ----------
    field_added : `bool`
        Whether any fields were already added.
    section_title : `str`
        The value the section's title should be.
    listing : `None | list<str>`
        The section's listing.
    
    Returns
    -------
    content : `str`
        The rendered content.
    field_added : `bool`
        Whether any fields were already added.
    """
    into, field_added = render_inline_listing_section_into([], field_added, section_title, listing)
    return ''.join(into), field_added
    
