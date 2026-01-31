__all__ = ()

from ..relationships_core import (
    RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK, RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
    RELATIONSHIP_TYPE_UNSET
)

from .relationship_listing_rendering_constants import (
    RELATIONSHIP_CONNECTION_TYPE_NAMES, RELATIONSHIP_LISTING_PAGE_SIZE, RELATIONSHIP_TITLES,
    RELATIONSHIP_TYPE_MASK_ORDER, RELATIONSHIP_TYPE_MODIFIER_SHIFTS
)


def create_relationship_listing_pages_wide(relationship_extension_traces, users, guild_id):
    """
    Creates relationship listing pages in a wide format.
    
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
    pages : `None | list<list<(tuple<(int, int, int)>, str)>>`
    """
    if (relationship_extension_traces is None):
        return None
    
    # Pre-group.
    user_relationships = []
    
    for relationship_extension_trace in relationship_extension_traces.values():
        user_id = relationship_extension_trace.user_id
        relationship_type = relationship_extension_trace.relationship_type
        
        values = []
        
        for index, mask in enumerate(RELATIONSHIP_TYPE_MASK_ORDER):
            if not (relationship_type & mask):
                continue
            
            # Find modifier_type.
            modifier_shift = RELATIONSHIP_TYPE_MODIFIER_SHIFTS.get(mask, 0)
            if not modifier_shift:
                modifier_type = RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE
            else:
                modifier_type = (relationship_type >> modifier_shift) & RELATIONSHIP_TYPE_CONNECTION_MODIFIER_MASK
            
            values.append(((index, mask, modifier_type)))
            continue
        
        if not values:
            values.append((
                (len(RELATIONSHIP_TYPE_MASK_ORDER) - 1),
                RELATIONSHIP_TYPE_UNSET,
                RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE,
            ),)
        
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
        
         
        user_relationships.append((tuple(values), user.name_at(guild_id)),)
        continue
    
    user_relationships.sort()
    
    # Create pages.
    pages = []
    page = None
    
    for relationship_item in user_relationships:
        if page is None:
            page = []
            pages.append(page)
            page_elements_available = RELATIONSHIP_LISTING_PAGE_SIZE
        
        page.append(relationship_item)
        page_elements_available -= 1
        
        # Reset page if empty
        if not page_elements_available:
            page = None
        
        continue
    
    return pages


def produce_relationships_listing_page_wide(page):
    """
    Produces a relationship listing page's content in wide format.
    
    Parameters
    ----------
    page : `list<(tuple<(int, int, int)>, str)>`
        The page to render.
    
    Yields
    ------
    part : `str`
    """
    line_added = False
    
    for values, user_name in page:
        if line_added:
            yield '\n'
        else:
            line_added = True
        
        yield '- '
        yield user_name
        yield ' - '
        
        relationship_name_added = False
        
        for index, relationship_type, relationship_type_modifier in values:
            if relationship_name_added:
                yield ' & '
            else:
                relationship_name_added = True
            
            yield RELATIONSHIP_TITLES[relationship_type][0]
            
            if relationship_type_modifier != RELATIONSHIP_TYPE_CONNECTION_MODIFIER_TYPE_NONE:
                yield ' ('
                yield RELATIONSHIP_CONNECTION_TYPE_NAMES[relationship_type_modifier]
                yield ')'
