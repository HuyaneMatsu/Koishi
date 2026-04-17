__all__ = ()

from ..relationships_core import (
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
    RELATIONSHIP_TYPE_UNSET
)

from .relationship_listing_rendering_constants import (
    RELATIONSHIP_CONNECTION_TYPE_NAMES, RELATIONSHIP_LISTING_PAGE_BREAK_GROUP_IF_LESS, RELATIONSHIP_LISTING_PAGE_SIZE,
    RELATIONSHIP_TITLES, RELATIONSHIP_TYPE_MASK_ORDER, RELATIONSHIP_TYPE_MODIFIER_SHIFTS
)


def create_relationship_listing_pages_legacy(relationship_extension_traces, users, guild_id):
    """
    Creates relationship listing pages in a legacy format.
    
    Parameters
    ----------
    relationship_extension_traces : ``None | dict<int, RelationshipExtensionTrace>``
        Relationship extension traces to render.
    
    users : ``None | list<ClientUserBase>``
        User of each relationship.
    
    guild_id : `int`
        The local guild's identifier.
    
    Returns
    -------
    pages : `None | list<list<(int, list<(int, str)>)>>`
    """
    if (relationship_extension_traces is None):
        return None
    
    # Pre-group.
    grouped_relationships = {}
    
    for relationship_extension_trace in relationship_extension_traces.values():
        user_id = relationship_extension_trace.user_id
        relationship_type = relationship_extension_trace.relationship_type
        
        best_mask = RELATIONSHIP_TYPE_UNSET
        best_relationship_type_modifier = RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE
        
        for mask in RELATIONSHIP_TYPE_MASK_ORDER:
            if not relationship_type & mask:
                continue
            
            # Find relationship_type_modifier.
            modifier_shift = RELATIONSHIP_TYPE_MODIFIER_SHIFTS.get(mask, 0)
            if not modifier_shift:
                relationship_type_modifier = RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE
            else:
                relationship_type_modifier = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
            
            # If the relation is not modified, we found the best match, break
            if relationship_type_modifier == RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE:
                best_mask = mask
                best_relationship_type_modifier = RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE
                break
            
            # If the relationship is modified, but we already have a better match, continue 
            if (
                (best_relationship_type_modifier != RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE) and
                (relationship_type_modifier >= best_relationship_type_modifier)
            ):
                continue
            
            best_mask = mask
            best_relationship_type_modifier = relationship_type_modifier
            continue
        
        try:
            group = grouped_relationships[best_mask]
        except KeyError:
            group = []
            grouped_relationships[best_mask] = group
        
        # Find user.
        if (users is None):
            user = None
        else:
            for user in users:
                if user.id == user_id:
                    break
            else:
                user = None
        
        if (user is None):
            raise RuntimeError(
                'Could not find a required user.', relationship_extension_traces, users, guild_id, user_id,
            )
        
        group.append((best_relationship_type_modifier, user.name_at(guild_id)))
        continue
    
    for group in grouped_relationships.values():
        group.sort()
    
    # Create pages.
    pages = []
    page = None
    
    for relationship_type in RELATIONSHIP_TYPE_MASK_ORDER:
        try:
            group = grouped_relationships[relationship_type]
        except KeyError:
            continue
        
        group_size = len(group)
        while True:
            if (
                (page is None) or
                (
                    (page_elements_available < RELATIONSHIP_LISTING_PAGE_BREAK_GROUP_IF_LESS) and
                    ((group_size + 2) > RELATIONSHIP_LISTING_PAGE_BREAK_GROUP_IF_LESS)
                )
            ):
                page = []
                pages.append(page)
                page_elements_available = RELATIONSHIP_LISTING_PAGE_SIZE
            
            if group_size < page_elements_available:
                page_elements_available = page_elements_available - group_size - 1
                group_to_add = group
                group = None
            
            else:
                cut_off = page_elements_available - 1
                page_elements_available = 0
                group_to_add = group[: cut_off]
                group = group[cut_off :]
                group_size -= cut_off
            
            page.append((relationship_type, group_to_add))
            
            # Reset the page if too small to add anything.
            if page_elements_available < 2:
                page = None
            
            if group is None:
                break
            
            continue
    
    return pages


def produce_relationships_listing_page_legacy(page):
    """
    Produces a relationship listing page's content in legacy format.
    
    Parameters
    ----------
    page : `list<(int, list<(int, str)>)>`
        The page to render.
    
    Yields
    ------
    part : `str`
    """
    line_added = False
    
    for relationship_type, group in page:
        if line_added:
            yield '\n'
        else:
            line_added = True
        
        yield '### '
        yield RELATIONSHIP_TITLES[relationship_type][len(group) > 1]
        
        for relationship_type_modifier, user_name in group:
            yield '\n- '
            yield user_name
            
            if relationship_type_modifier != RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE:
                yield ' ('
                yield RELATIONSHIP_CONNECTION_TYPE_NAMES[relationship_type_modifier]
                yield ')'
