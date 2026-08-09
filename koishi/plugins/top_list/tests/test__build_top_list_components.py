import vampytest
from hata import Component, User, create_button, create_row, create_separator, create_text_display

from ..component_building import build_top_list_components
from ..constants import (
    EMOJI_CLOSE, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, STYLE_NAME, STYLE_NUMBER, STYLE_VALUE, TOP_LIST_TYPE_CREDIBILITY
)


def _iter_options():
    user_id_0 = 202608090020
    user_id_1 = 202608090021
    user_id_2 = 202608090022
    
    yield (
        user_id_0,
        TOP_LIST_TYPE_CREDIBILITY,
        10,
        [],
        False,
        0,
        [
            create_text_display(
                '# Credibility top-list\n'
                '\n'
                'Page: 11'
            ),
            create_separator(),
            create_row(
                create_button(
                    f'Page 10',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = f'top_list.page.{user_id_0:x}.{TOP_LIST_TYPE_CREDIBILITY:x}.{9:x}',
                    enabled = True,
                ),
                create_button(
                    f'Page 12',
                    EMOJI_PAGE_NEXT,
                    custom_id = f'top_list.page.i.d',
                    enabled = False,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'top_list.close.{user_id_0:x}',
                    enabled = True,
                ),
            )
        ],
    )
    
    yield (
        user_id_0,
        TOP_LIST_TYPE_CREDIBILITY,
        0,
        [
            (User.precreate(user_id_1, name = 'okuu'), 1112),
            (User.precreate(user_id_2, name = 'orin'), 1111),
        ],
        True,
        0,
        [
            create_text_display(
                '# Credibility top-list\n'
                '\n'
                'Page: 1'
            ),
            create_separator(),
            create_text_display(
                f'```ansi\n'
                f'{STYLE_NUMBER}1.: {STYLE_VALUE}{1112!s} {STYLE_NAME}okuu\n'
                f'{STYLE_NUMBER}2.: {STYLE_VALUE}{1111!s} {STYLE_NAME}orin\n'
                f'```'
            ),
            create_separator(),
            create_row(
                create_button(
                    f'Page 0',
                    EMOJI_PAGE_PREVIOUS,
                    custom_id = f'top_list.page.d.d',
                    enabled = False,
                ),
                create_button(
                    f'Page 2',
                    EMOJI_PAGE_NEXT,
                    custom_id = f'top_list.page.{user_id_0:x}.{TOP_LIST_TYPE_CREDIBILITY:x}.{1:x}',
                    enabled = True,
                ),
                create_button(
                    'Close',
                    EMOJI_CLOSE,
                    custom_id = f'top_list.close.{user_id_0:x}',
                    enabled = True,
                ),
            )
        ],
    )


@vampytest._(vampytest.call_from(_iter_options()).returning_last())
def test__build_top_list_components(user_id, top_list_type, page_index, processed_entries, has_more, guild_id):
    """
    Tests whether ``build_top_list_components`` works as intended.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    top_list_type : `int`
        Top list's type.
    
    page_index : `int`
        Page index.
    
    processed_entries : ``list<(ClientUserBase, int)>``
        Professed entries.
    
    has_more : `bool`
        Whether there are more entries.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    output : ``list<Component>``
    """
    output = build_top_list_components(user_id, top_list_type, page_index, processed_entries, has_more, guild_id)
    vampytest.assert_instance(output, list)
    for element in output:
        vampytest.assert_instance(element, Component)
    return output
