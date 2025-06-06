__all__ = ()

from hata import create_button, create_row

from .constants import (
    CUSTOM_ID_INVENTORY_PAGE_CLOSE, CUSTOM_ID_INVENTORY_PAGE_DISABLED_DECREMENT,
    CUSTOM_ID_INVENTORY_PAGE_DISABLED_INCREMENT, CUSTOM_ID_INVENTORY_PAGE_N_BUILDER, EMOJI_CLOSE, EMOJI_LEFT,
    EMOJI_RIGHT
)


def build_component_switch_page(sort_by, sort_order, page_index, page_count):
    """
    Builds a component allowing switching pages.
    
    Parameters
    ----------
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_index : `int`
        The current page's index.
    
    page_count : `int`
        Amount of pages.
    
    Returns
    -------
    component : ``Component``
    """
    if page_index:
        button_left = create_button(
            f'Page {page_index}',
            EMOJI_LEFT,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_N_BUILDER(sort_by, sort_order, page_index - 1),
        )
    else:
        button_left = create_button(
            'Page 0',
            EMOJI_LEFT,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_DISABLED_DECREMENT,
            enabled = False,
        )
    
    if page_index < page_count - 1:
        button_right = create_button(
            f'Page {page_index + 2}',
            EMOJI_RIGHT,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_N_BUILDER(sort_by, sort_order, page_index + 1),
        )
    else:
        button_right = create_button(
            f'Page {page_index + 2}',
            EMOJI_RIGHT,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_DISABLED_INCREMENT,
            enabled = False,
        )
    
    return create_row(
        button_left,
        button_right,
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_CLOSE,
        ),
    )
