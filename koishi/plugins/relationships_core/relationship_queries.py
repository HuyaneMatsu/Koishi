__all__ = ('get_relationship_listing', 'get_relationship_listing_and_extend')

from scarletio import copy_docs
from sqlalchemy import or_

from ...bot_utils.models import DB_ENGINE, RELATIONSHIP_TABLE, relationship_model

from .constants import RELATIONSHIP_CACHE_LISTING, RELATIONSHIP_CACHE_LISTING_SIZE_MAX
from .helpers import iter_select_relationships
from .relationship import Relationship
from .relationship_types import RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS, RELATION_TYPE_ALLOWED_EXTENDS


async def get_relationship_listing(user_id):
    """
    Gets the user's relationships.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    relationship_listing : `None | list<Relationship>`
    """
    listing_key = user_id
    
    try:
        listing = RELATIONSHIP_CACHE_LISTING[user_id]
    except KeyError:
        pass
    else:
        RELATIONSHIP_CACHE_LISTING.move_to_end(user_id)
        return listing
    
    listing = await query_relationship_listing(user_id)
    RELATIONSHIP_CACHE_LISTING[listing_key] = listing
    if len(RELATIONSHIP_CACHE_LISTING) > RELATIONSHIP_CACHE_LISTING_SIZE_MAX:
        del RELATIONSHIP_CACHE_LISTING[next(iter(RELATIONSHIP_CACHE_LISTING))]
        
    return listing


def _iter_user_ids_from(user_relationship_listing, user_relationship_listing_extend):
    """
    Iterates over all user identifiers in the given relationship listings.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_relationship_listing : `list<Relationship>`
        The source user's relationships.
    
    user_relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        The relationship extends to get the user identifiers from.
    
    Yields
    ------
    user_id : `int`
    """
    for relationship in user_relationship_listing:
        yield relationship.source_user_id
        yield relationship.target_user_id
    
    if (user_relationship_listing_extend is not None):
        for extender_relationship, relationship_listing in user_relationship_listing_extend:
            for relationship in relationship_listing:
                yield relationship.source_user_id
                yield relationship.target_user_id


def _select_extended_relationships(
    allowed_relationship_types,
    user_relationship_listing,
    user_relationship_listing_extend,
    connector_user_id,
    relationship_listing,
):
    """
    Selects the extended relationships.
    
    Parameters
    ----------
    allowed_relationship_types : `tuple<int>`
        The allowed relationship types to be connected.
    
    user_relationship_listing : `list<Relationship>`
        The source user's relationships.
    
    user_relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        The relationship extends to get the user identifiers from.
    
    connector_user_id : `int`
        The connector user's identifier.
    
    relationship_listing : `list<Relationship>`
        The waifu user's relationships.
    
    Returns
    -------
    extra : `None | list<Relationship>`
    """
    extra = None
    
    for relationship in relationship_listing:
        # Exclude duplicate users.
        related_id = relationship.source_user_id
        relationship_type = relationship.relationship_type
        if related_id == connector_user_id:
            related_id = relationship.target_user_id
            relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
        
        if relationship_type not in allowed_relationship_types:
            continue
        
        # Exclude if the user is already related.
        if any(
            related_id == user_id for user_id
            in _iter_user_ids_from(user_relationship_listing, user_relationship_listing_extend)
        ):
            continue
        
        if extra is None:
            extra = []
            
        extra.append(relationship)
    
    return extra


async def get_relationship_listing_and_extend(user_id):
    """
    Gets the user's extended relationship listing.
    The extend is separated by the relationships they are branching out form.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    relationship_listing : `None | list<Relationship>`
    relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
    """
    user_relationship_listing = await get_relationship_listing(user_id)
    if (user_relationship_listing is None):
        return None, None
    
    user_relationship_listing_extend = None
    
    for extender_relationship_type, allowed_relationship_types in RELATION_TYPE_ALLOWED_EXTENDS:
        for relationship in iter_select_relationships(user_id, extender_relationship_type, user_relationship_listing):
            connector_user_id = relationship.source_user_id
            if connector_user_id == user_id:
                connector_user_id = relationship.target_user_id
            
            relationship_listing = await get_relationship_listing(connector_user_id)
            if (relationship_listing is None) or (len(relationship_listing) == 1):
                continue
            
            extra = _select_extended_relationships(
                allowed_relationship_types,
                user_relationship_listing,
                user_relationship_listing_extend,
                connector_user_id,
                relationship_listing,
            )
            
            if extra is None:
                continue
            
            if user_relationship_listing_extend is None:
                user_relationship_listing_extend = []
            
            user_relationship_listing_extend.append((relationship, extra))
    
    return user_relationship_listing, user_relationship_listing_extend


async def query_relationship_listing(user_id):
    """
    queries the user's relationships.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    Returns
    -------
    relationship_listing : `None | list<Relationship>`
    """
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            RELATIONSHIP_TABLE.select().where(
                or_(
                    relationship_model.source_user_id == user_id,
                    relationship_model.target_user_id == user_id,
                ),  
            ),
        )
        
        results = await response.fetchall()
        if results:
            relationships = [Relationship.from_entry(result) for result in results]
        else:
            relationships = None
    
    return relationships


if DB_ENGINE is None:
    @copy_docs(query_relationship_listing)
    async def query_relationship_listing(user_id):
        return None
