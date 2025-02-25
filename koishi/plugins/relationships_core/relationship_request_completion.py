__all__ = (
    'autocomplete_relationship_request_source_user_name', 'autocomplete_relationship_request_target_user_name',
    'get_relationship_request', 'get_relationship_request_and_user_like_at'
)

from hata.ext.slash import abort

from ...bot_utils.user_getter import get_users_unordered

from .completion_helpers import looks_like_user_id, _make_suggestions
from .relationship_request_queries import get_relationship_request_listing


def _iter_relationship_request_user_ids_to_request(outgoing, relationship_requests):
    """
    Iterates over the relationship requests users' identifiers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    outgoing : `bool`
        Whether to auto complete the outgoing users.
    
    relationship_requests : `list<RelationshipRequest>`
        The relationship requests to get the user identifiers from.
    
    Yields
    ------
    user_id : `int`
    """
    for relationship_request in relationship_requests:
        if outgoing:
            user_id = relationship_request.target_user_id
        else:
            user_id = relationship_request.source_user_id
        
        yield user_id


async def get_relationship_request_user_names_like_at(user_id, outgoing, value, guild_id):
    """
    Helper function for auto completing relationship request names.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who is requesting.
    
    outgoing : `bool`
        Whether to auto complete the outgoing users.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    suggestions : `None | list<(str, str)>`
    """
    relationship_requests = await get_relationship_request_listing(user_id, outgoing)
    if relationship_requests is None:
        return None
    
    users = await get_users_unordered(_iter_relationship_request_user_ids_to_request(outgoing, relationship_requests))
    
    return _make_suggestions(users, value, guild_id)


async def get_relationship_request_and_user_like_at(user_id, outgoing, value, guild_id):
    """
    Helper function for getting a single user with a name like the given one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who is requesting.
    
    outgoing : `bool`
        Whether to auto complete the outgoing users.
    
    value : `None | str`
        The value to get user name for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    relationship_request_and_user : `(RelationshipRequest, ClientUserBase)`
    
    Raises
    ------
    InteractionAbortedError
    """
    while True:
        if value is None:
            break
        
        relationship_requests = await get_relationship_request_listing(user_id, outgoing)
        if relationship_requests is None:
            break
        
        users = await get_users_unordered(
            _iter_relationship_request_user_ids_to_request(outgoing, relationship_requests)
        )
        
        
        if not looks_like_user_id(value):
            user = None
        
        else:
            passed_user_id = int(value)
            for user in users:
                if user.id == passed_user_id:
                    break
            else:
                user = None
        
        if user is None:
            for user in users:
                if user.has_name_like_at(value, guild_id):
                    break
            else:
                break
        
        relationship_request = next(
            relationship_request for relationship_request in relationship_requests
            if (relationship_request.target_user_id if outgoing else relationship_request.source_user_id) == user.id
        )
        
        return relationship_request, user
    
    abort('Could not match anyone.')


async def autocomplete_relationship_request_source_user_name(event, value):
    """
    Autocompletes a relationship request's source user name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value to auto complete.
    
    Returns
    -------
    suggestions : `None | list<(str, int)>`
    """
    return await get_relationship_request_user_names_like_at(event.user_id, False, value, event.guild_id)


async def autocomplete_relationship_request_target_user_name(event, value):
    """
    Autocompletes a relationship request's target user name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value to auto complete.
    
    Returns
    -------
    suggestions : `None | list<(str, int)>`
    """
    return await get_relationship_request_user_names_like_at(event.user_id, True, value, event.guild_id)


async def get_relationship_request(source_user_id, target_user_id):
    """
    gets a relationship request for the given user identifier combination.
    
    This function is a coroutine.
    
    Parameters
    ----------
    source_user_id : `int`
        Source user identifier to get relationships for.
    
    target_user_id : `int`
        The target user's identifier.
    
    Raises
    ------
    InteractionAbortedError
    """
    relationship_proposal_listing = await get_relationship_request_listing(source_user_id, True)
    
    if relationship_proposal_listing is not None:
        for relationship_proposal in relationship_proposal_listing:
            if relationship_proposal.target_user_id == target_user_id:
                return relationship_proposal
    
    abort('Could not match anyone.')
