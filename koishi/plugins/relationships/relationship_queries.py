__all__ = ('get_relationship_listing', 'get_relationship_listing_and_extend')

from scarletio import copy_docs
from sqlalchemy import or_

from ...bot_utils.models import DB_ENGINE, RELATIONSHIP_TABLE, relationship_model

from .constants import RELATIONSHIP_CACHE_LISTING, RELATIONSHIP_CACHE_LISTING_SIZE_MAX
from .helpers import select_relationship
from .relationship import Relationship
from .relationship_types import RELATIONSHIP_TYPE_MASTER, RELATIONSHIP_TYPE_MAID, RELATIONSHIP_TYPE_WAIFU


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


def _filter_extended_relationships(user_relationship_listing, waifu_id, waifu_relationship_listing):
    """
    Filters down the extended relationships.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    user_relationship_listing : `list<Relationship>`
        The source user's relationships.
    
    waifu_id : `int`
        The waifu user's identifier.
    
    waifu_relationship_listing : `list<Relationship>`
        The waifu user's relationships.
    
    Yields
    ------
    relationship : ``Relationship``
    """
    for relationship in waifu_relationship_listing:
        # Waifu ones are always duplicate.
        relationship_type = relationship.relationship_type
        if relationship_type == RELATIONSHIP_TYPE_WAIFU:
            continue
        
        # Exclude waifu's master.
        if (
            (relationship_type == RELATIONSHIP_TYPE_MASTER and relationship.target_user_id == waifu_id) or 
            (relationship_type == RELATIONSHIP_TYPE_MAID and relationship.source_user_id == waifu_id)
        ):
            continue
        
        # Exclude duplicate users.
        related_id = relationship.source_user_id
        if related_id == waifu_id:
            related_id = relationship.target_user_id
        
        # Exclude if the original user is already related.
        if any(
            ((relationship.source_user_id == related_id) or (relationship.target_user_id == related_id))
            for relationship in user_relationship_listing
        ):
            continue
        
        yield relationship
        continue


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
    
    waifu_relationship = select_relationship(user_id, RELATIONSHIP_TYPE_WAIFU, user_relationship_listing)
    if (waifu_relationship is None):
        return user_relationship_listing, None
    
    waifu_id = waifu_relationship.source_user_id
    if waifu_id == user_id:
        waifu_id = waifu_relationship.target_user_id
    
    waifu_relationship_listing = await get_relationship_listing(waifu_id)
    if (waifu_relationship_listing is None) or (len(waifu_relationship_listing) == 1):
        return user_relationship_listing, None
    
    relationship_listing_extend = None
    
    extra = None
    for relationship in _filter_extended_relationships(user_relationship_listing, waifu_id, waifu_relationship_listing):
        if extra is None:
            extra = []
        
        extra.append(relationship)
    
    if (extra is not None):
        if (relationship_listing_extend is None):
            relationship_listing_extend = []
        
        relationship_listing_extend.append((waifu_relationship, extra),)
    
    return user_relationship_listing, relationship_listing_extend


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
