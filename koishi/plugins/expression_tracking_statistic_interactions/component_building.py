__all__ = ()

from hata import (
    create_button, create_text_display, create_row, create_section, create_separator, create_thumbnail_media
)
from .constants import EMOJI_CLOSE, EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, MODE_GUILD_IN, MODE_GUILD_OF
from .content_building import produce_guild_in_description, produce_guild_of_description, produce_header
from .custom_ids import (
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_CLOSE_BUILDER,
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_DECREMENT_DISABLED,
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_INCREMENT_DISABLED,
    CUSTOM_ID_EXPRESSION_TRACKING_STATISTIC_VIEW_BUILDER,
)


def build_components(
    client,
    user,
    guild,
    entries,
    page_count,
    mode,
    action_types_packed,
    entity_filter_rule,
    months,
    page_index,
    page_size,
    order_decreasing,
):
    """
    Builds expression tracking components.
    
    Parameters
    ----------
    client : ``ClientUserBase``
        The client rendering this message.
    
    user : ``ClientUserBase``
        The user invoking this interaction.
    
    guild : ``None | Guild``
        The guild in context.
    
    entries : `list<tuple<int>>`
        Entries to render.
    
    page_count : `int`
        The amount of pages.
    
    mode : `int`
        The usage mode to respond with.
    
    action_types_packed : `int`
        The action types packed.
    
    entity_filter_rule : `int`
        Entity filter rule for detailed filtering.
    
    months : `int`
        The amount of months to look back.
    
    page_index : `int`
        The page's index to display.
    
    page_size : `int`
        The page's size to display.
    
    order_decreasing : `bool`
        Whether to order in a decreasing order.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Add header
    header_text_display = create_text_display(''.join([*produce_header(
        guild, mode, action_types_packed, entity_filter_rule, months, page_index, page_size, order_decreasing
    )]))
    
    while True:
        if (mode == MODE_GUILD_OF) or (mode == MODE_GUILD_IN):
            if guild is not None:
                icon_url = guild.icon_url
                break
        
        icon_url = None
        break
    
    if icon_url is None:
        header_component = header_text_display
    else:
        header_component = create_section(
            header_text_display,
            thumbnail = create_thumbnail_media(icon_url),
        )
    
    components.append(header_component)
    components.append(create_separator())
    
    # Add entries if any
    if entries:
        if mode == MODE_GUILD_OF:
            description = ''.join([*produce_guild_of_description(
                client,
                action_types_packed,
                entries,
            )])
        elif mode == MODE_GUILD_IN:
            description = ''.join([*produce_guild_in_description(
                client,
                (0 if guild is None else guild.id),
                action_types_packed,
                entries,
            )])
        else:
            description = '*nothing*'
        components.append(create_text_display(description))
        components.append(create_separator())
    
    # Add control
    if mode == MODE_GUILD_OF or mode == MODE_GUILD_IN:
        entry_id = (0 if guild is None else guild.id)
    else:
        entry_id = 0
    
    if page_index <= 0:
        custom_id_page_index_decrement = CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_DECREMENT_DISABLED
        component_page_index_decrement_enabled = False
    else:
        custom_id_page_index_decrement = CUSTOM_ID_EXPRESSION_TRACKING_STATISTIC_VIEW_BUILDER(
            user.id,
            mode,
            entry_id,
            action_types_packed,
            entity_filter_rule,
            months,
            (page_index - 1),
            page_size,
            order_decreasing,
        )
        component_page_index_decrement_enabled = True
    
    if (page_index + 1) >= page_count:
        custom_id_page_index_increment = CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_PAGE_INDEX_INCREMENT_DISABLED
        component_page_index_increment_enabled = False
    else:
        custom_id_page_index_increment = CUSTOM_ID_EXPRESSION_TRACKING_STATISTIC_VIEW_BUILDER(
            user.id,
            mode,
            entry_id,
            action_types_packed,
            entity_filter_rule,
            months,
            (page_index + 1),
            page_size,
            order_decreasing,
        )
        component_page_index_increment_enabled = True
    
    components.append(create_row(
        create_button(
            f'Page {page_index!s}',
            EMOJI_PAGE_PREVIOUS,
            custom_id = custom_id_page_index_decrement,
            enabled = component_page_index_decrement_enabled,
        ),
        create_button(
            f'Page {page_index + 2!s}',
            EMOJI_PAGE_NEXT,
            custom_id = custom_id_page_index_increment,
            enabled = component_page_index_increment_enabled,
        ),
        create_button(
            'Close',
            EMOJI_CLOSE,
            custom_id = CUSTOM_ID_EXPRESSION_TRACKING_STATISTICS_CLOSE_BUILDER(user.id),
        )
    ))
    
    # Return
    return components
