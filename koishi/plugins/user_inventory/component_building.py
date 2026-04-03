__all__ = ()

from hata import (
    create_button, create_row, create_section, create_separator, create_text_display, create_thumbnail_media
)

from .constants import (
    CUSTOM_ID_INVENTORY_PAGE_CLOSE, CUSTOM_ID_INVENTORY_PAGE_DISABLED_DECREMENT,
    CUSTOM_ID_INVENTORY_PAGE_DISABLED_INCREMENT, CUSTOM_ID_INVENTORY_PAGE_N_BUILDER, EMOJI_CLOSE, EMOJI_LEFT,
    EMOJI_REFRESH, EMOJI_RIGHT
)
from .content_building import produce_inventory_description, produce_inventory_header


def build_inventory_view_components(
    user, guild_id, item_entries, sort_by, sort_order, page_index, page_count, weight, capacity
):
    """
    Builds a component allowing switching pages.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The user who's inventory is being rendered.
    
    guild_id : `int`
        The local guild's identifier.
    
    item_entries : `None | dict<int, ItemEntry>`
        The items of the user.
    
    sort_by : `int`
        Identifier to determine how item entries should be sorted.
    
    sort_order : `int`
        Identifier to determine sorting order.
    
    page_index : `int`
        The current page's index.
    
    page_count : `int`
        Amount of pages.
    
    weight : `int`
        The weight of the inventory.
    
    capacity : `int`
        Inventory capacity.
    
    Returns
    -------
    components : ``listComponent>``
    """
    components = []
    
    # Header
    components.append(create_section(
        create_text_display(''.join([*produce_inventory_header(
            user, guild_id, page_index, sort_by, sort_order, weight, capacity
        )])),
        thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
    ))
    components.append(create_separator())
    
    # Items
    if item_entries:
        components.append(create_text_display(''.join([*produce_inventory_description(item_entries)])))
        components.append(create_separator())
    
    # Control
    if page_index:
        button_left = create_button(
            f'Page {page_index}',
            EMOJI_LEFT,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_N_BUILDER(user.id, sort_by, sort_order, page_index - 1),
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
            custom_id = CUSTOM_ID_INVENTORY_PAGE_N_BUILDER(user.id, sort_by, sort_order, page_index + 1),
        )
    else:
        button_right = create_button(
            f'Page {page_index + 2}',
            EMOJI_RIGHT,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_DISABLED_INCREMENT,
            enabled = False,
        )
    
    components.append(create_row(
        create_button(
            'Refresh',
            EMOJI_REFRESH,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_N_BUILDER(user.id, sort_by, sort_order, page_index)
        ),
        button_left,
        button_right,
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_INVENTORY_PAGE_CLOSE,
        ),
    ))
    
    return components
