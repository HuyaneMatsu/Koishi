__all__ = ('get_relationship_request_listing',)

from scarletio import copy_docs

from ...bot_utils.models import DB_ENGINE, RELATIONSHIP_REQUEST_TABLE, relationship_request_model

from .constants import RELATIONSHIP_REQUEST_CACHE_LISTING, RELATIONSHIP_REQUEST_CACHE_LISTING_SIZE_MAX
from .relationship_request import RelationshipRequest


async def get_relationship_request_listing(user_id, outgoing):
    """
    Gets the relationship request entries for the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    outgoing : `bool`
        Whether to query for the outgoing requests.
    
    Returns
    -------
    entries : `None | list<RelationshipRequest>`
    """
    listing_key = user_id, outgoing
    
    try:
        listing = RELATIONSHIP_REQUEST_CACHE_LISTING[listing_key]
    except KeyError:
        pass
    else:
        RELATIONSHIP_REQUEST_CACHE_LISTING.move_to_end(listing_key)
        return listing
    
    listing = await query_relationship_request_listing(user_id, outgoing)
    RELATIONSHIP_REQUEST_CACHE_LISTING[listing_key] = listing
    if len(RELATIONSHIP_REQUEST_CACHE_LISTING) > RELATIONSHIP_REQUEST_CACHE_LISTING_SIZE_MAX:
        del RELATIONSHIP_REQUEST_CACHE_LISTING[next(iter(RELATIONSHIP_REQUEST_CACHE_LISTING))]
    
    return listing


async def query_relationship_request_listing(user_id, outgoing):
    """
    Queries the relationship request entries for the given user.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        User's identifier.
    
    outgoing : `bool`
        Whether to query for the outgoing requests.
    
    Returns
    -------
    entries : `None | list<RelationshipRequest>`
    """
    if outgoing:
        user_id_member = relationship_request_model.source_user_id
    else:
        user_id_member = relationship_request_model.target_user_id
    
    async with DB_ENGINE.connect() as connector:
        response = await connector.execute(
            RELATIONSHIP_REQUEST_TABLE.select().where(
                user_id_member == user_id,
            ),
        )
        
        results = await response.fetchall()
        if results:
            relationship_requests = [RelationshipRequest.from_entry(result) for result in results]
        else:
            relationship_requests = None
    
    return relationship_requests


if DB_ENGINE is None:
    @copy_docs(query_relationship_request_listing)
    async def query_relationship_request_listing(user_id, outgoing):
        return None
