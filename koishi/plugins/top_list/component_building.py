__all__ = ()

from hata import create_button, create_row, create_separator, create_text_display

from .constants import EMOJI_CLOSE, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS
from .content_building import produce_top_list_description, produce_top_list_header
from .custom_ids import (
    CUSTOM_ID_TOP_LIST_CLOSE_BUILDER, CUSTOM_ID_TOP_LIST_PAGE_INDEX_BUILDER,
    CUSTOM_ID_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED, CUSTOM_ID_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED
)


def build_top_list_components(user_id, top_list_type, page_index, processed_entries, has_more, guild_id):
    """
    Builds top list components.
    
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
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_text_display(
        ''.join([*produce_top_list_header(top_list_type, page_index)])
    ))
    components.append(create_separator())
    
    # Description
    
    if processed_entries:
        components.append(create_text_display(
            ''.join([*produce_top_list_description(page_index, processed_entries, guild_id)])
        ))
        components.append(create_separator())
    
    # Control
    
    if page_index:
        component_page_index_decrement_custom_id = CUSTOM_ID_TOP_LIST_PAGE_INDEX_BUILDER(
            user_id, top_list_type, page_index - 1
        )
        component_page_index_decrement_enabled = True
    else:
        component_page_index_decrement_custom_id = CUSTOM_ID_TOP_LIST_PAGE_INDEX_DECREMENT_DISABLED
        component_page_index_decrement_enabled = False
    
    if has_more:
        component_page_index_increment_custom_id = CUSTOM_ID_TOP_LIST_PAGE_INDEX_BUILDER(
            user_id, top_list_type, page_index + 1
        )
        component_page_index_increment_enabled = True
    else:
        component_page_index_increment_custom_id = CUSTOM_ID_TOP_LIST_PAGE_INDEX_INCREMENT_DISABLED
        component_page_index_increment_enabled = False
    
    components.append(create_row(
        create_button(
            f'Page {page_index}',
            EMOJI_PAGE_PREVIOUS,
            custom_id = component_page_index_decrement_custom_id,
            enabled = component_page_index_decrement_enabled,
        ),
        create_button(
            f'Page {page_index + 2}',
            EMOJI_PAGE_NEXT,
            custom_id = component_page_index_increment_custom_id,
            enabled = component_page_index_increment_enabled,
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_TOP_LIST_CLOSE_BUILDER(user_id),
            enabled = True,
        ),
    ))
    
    return components
