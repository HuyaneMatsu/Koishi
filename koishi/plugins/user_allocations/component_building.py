__all__ = ()

from hata import (
    create_button, create_row, create_section, create_separator, create_text_display, create_thumbnail_media
)

from ..user_balance import ALLOCATION_FEATURE_ID_GAME_21

from .component_building_game_21 import build_game_21_detailed_components, build_game_21_entry_component
from .component_building_unknown import build_unknown_detailed_components, build_unknown_entry_component
from .constants import EMOJI_PAGE_NEXT, EMOJI_PAGE_PREVIOUS, EMOJI_REFRESH
from .custom_ids import (
    USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_DECREMENT_DISABLED,
    USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_INCREMENT_DISABLED, USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER
)


def build_view_components(user, page_index, page_count, guild_id, allocations):
    """
    Builds view components.
    
    Parameters
    ----------
    user : ``ClientUserBase``
        The invoking user.
    
    page_index : `int`
        The current page's index.
    
    page_count : `int`
        The amount of pages.
    
    guild_id : `int`
        The local guild's identifier.
    
    allocations : `list<(int, int, int)>`
        The user's allocations.
    
    Returns
    -------
    components : ``list<Component>``
    """
    components = []
    
    # Header
    
    components.append(create_section(
        create_text_display(f'# {user.name_at(guild_id)}\'s allocations'),
        thumbnail = create_thumbnail_media(user.avatar_url_at(guild_id)),
    ))
    
    components.append(create_separator())
    
    # Listing
    
    if allocations:
        
        for allocation_feature_id, allocation_session_id, allocation_amount in allocations:
            if allocation_feature_id == ALLOCATION_FEATURE_ID_GAME_21:
                component_builder = build_game_21_entry_component
            else:
                component_builder = build_unknown_entry_component
            
            components.append(component_builder(user.id, page_index, allocation_session_id, allocation_amount))
        
        components.append(create_separator())
    
    # Control
    
    if page_index:
        custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER(user.id, page_index - 1)
        enabled = True
    else:
        custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_DECREMENT_DISABLED
        enabled = False
        
    component_page_index_decrement = create_button(
        f'Page {page_index}',
        EMOJI_PAGE_PREVIOUS,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    if page_index < page_count - 1:
        custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER(user.id, page_index + 1)
        enabled = True
    else:
        custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_INDEX_INCREMENT_DISABLED
        enabled = False
        
    component_page_index_increment = create_button(
        f'Page {page_index + 2}',
        EMOJI_PAGE_NEXT,
        custom_id = custom_id,
        enabled = enabled,
    )
    
    components.append(create_row(
        create_button(
            'Refresh',
            EMOJI_REFRESH,
            custom_id = USER_ALLOCATIONS_CUSTOM_ID_VIEW_PAGE_BUILDER(user.id, page_index),
        ),
        component_page_index_decrement,
        component_page_index_increment,
    ))
    
    return components


def build_details_components(user_id, page_index, allocation_feature_id, session_id, amount, session, guild_id):
    """
    Builds the details components.
    
    Parameters
    ----------
    user_id : `int`
        The invoking user's identifier.
    
    page_index : `int`
        Page index to redirect to.
    
    allocation_feature_id : `int`
        The allocation feature's identifier.
    
    session_id : `int`
        The session's identifier.
    
    amount : `int`
        The allocated amount.
    
    session : `None | object`
        The game's session.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    components : ``list<Component>``
    """
    if allocation_feature_id == ALLOCATION_FEATURE_ID_GAME_21:
        component_builder = build_game_21_detailed_components
    else:
        component_builder = build_unknown_detailed_components
    
    return component_builder(user_id, page_index, session_id, amount, session, guild_id)
