__all__ = (
    'get_extender_relationship_and_relationship_and_user_like_at',
    'iter_relationship_and_extend_user_ids_to_request',
)

from hata.ext.slash import abort

from ...bot_utils.constants import RELATIONSHIP_VALUE_DEFAULT
from ...bot_utils.user_getter import get_users_unordered

from .completion_helpers import _make_suggestions
from .relationship_queries import get_relationship_listing, get_relationship_listing_and_extend
from .relationship_types import RELATIONSHIP_TYPE_UNSET


def _iter_relationship_user_ids_to_request(excluded_user_id, relationships):
    """
    Iterates over the relationship users' identifiers.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    excluded_user_id : `int`
        The user identifier to exclude.
    
    relationships : `list<Relationship>`
        The relationships to get the user identifiers from.
    
    Yields
    -------
    user_id : `int`
    """
    for relationship in relationships:
        user_id = relationship.source_user_id
        if user_id == excluded_user_id:
            user_id = relationship.target_user_id
        
        yield user_id


def iter_relationship_and_extend_user_ids_to_request(
    excluded_user_id, relationship_listing, relationship_listing_extend
):
    """
    Iterates over the relationship's and their extends' users' identifiers.
    
    This function is a coroutine.
    
    Parameters
    ----------
    excluded_user_id : `int`
        The user identifier to exclude.
    
    relationship_listing : `list<Relationship>`
        The relationships to get the user identifiers from.
    
    relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        The relationship extends to get the user identifiers from.
    
    Yields
    -------
    user_id : `int`
    """
    yield from _iter_relationship_user_ids_to_request(excluded_user_id, relationship_listing)
    
    if (relationship_listing_extend is not None):
        for extender_relationship, relationship_listing_extend in relationship_listing_extend:
            user_id = extender_relationship.source_user_id
            if user_id == excluded_user_id:
                user_id = extender_relationship.target_user_id
            
            yield from _iter_relationship_user_ids_to_request(user_id, relationship_listing_extend)


def _filter_relationships_unset_outgoing(user_id, relationships):
    """
    Filters out the unset outgoing relationships.
    
    Parameters
    ----------
    user_id : `int`
        User identifier to check their side of the relationships.
    
    relationships : `list<Relationship>`
        Relationships to filter from.
    
    Returns
    -------
    relationships : `None | list<Relationship>`
    """
    filtered_relationships = None
    
    for relationship in relationships:
        if relationship.relationship_type != RELATIONSHIP_TYPE_UNSET:
            continue
        
        if relationship.source_user_id == user_id:
            relationship_value = relationship.source_investment
        else:
            relationship_value = relationship.target_investment
        
        if relationship_value < RELATIONSHIP_VALUE_DEFAULT:
            continue
        
        if filtered_relationships is None:
            filtered_relationships = []
        
        filtered_relationships.append(relationship)
    
    return filtered_relationships


def _select_first_relationship_and_user(relationships, users, value, guild_id):
    """
    Selects the first matching user and returns its relationship & the user as well of course.
    
    Parameters
    ----------
    relationships : `list<Relationship>`
        Relationships to filter from.
    
    users : `list<ClientUserBase>`
        The users to filter from.
    
    value : `None | str`
        Value to filter for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    relationship_and_user : `None | (Relationship, ClientUserBase)`
    """
    for user in users:
        if user.has_name_like_at(value, guild_id):
            break
    else:
        return None
    
    user_id = user.id
    
    for relationship in relationships:
        if (relationship.source_user_id == user_id) or (relationship.target_user_id == user_id):
            break
    else:
        return None
    
    return relationship, user


def _select_first_extender_relationship_and_relationship_and_user(
    relationship_listing, relationship_listing_extend, users, value, guild_id
):
    """
    Selects the first matching user and returns its relationship & the user as well of course.
    
    Parameters
    ----------
    relationship_listing : `list<Relationship>`
        The relationships to get the user identifiers from.
    
    relationship_listing_extend : `None | list<(Relationship, list<Relationship>)>`
        The relationship extends to get the user identifiers from.
    
    users : `list<ClientUserBase>`
        The users to filter from.
    
    value : `None | str`
        Value to filter for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    extender_relationship_and_relationship_and_user : `None | (None | Relationship, Relationship, ClientUserBase)`
    """
    for user in users:
        if user.has_name_like_at(value, guild_id):
            break
    else:
        return None
    
    user_id = user.id
    
    for relationship in relationship_listing:
        if (relationship.source_user_id == user_id) or (relationship.target_user_id == user_id):
            extender_relationship = None
            break
    else:
        if (relationship_listing_extend is None):
            return None
        
        for extender_relationship, relationship_listing_extend in relationship_listing_extend:
            for relationship in relationship_listing_extend:
                if (relationship.source_user_id == user_id) or (relationship.target_user_id == user_id):
                    break
            else:
                continue
            break
        else:
            return None
    
    return extender_relationship, relationship, user


async def get_relationship_user_names_like_at(user_id, value, guild_id):
    """
    Helper function for auto completing relationship user names.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who ising.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    relationships = await get_relationship_listing(user_id)
    if relationships is None:
        return None
    
    users = await get_users_unordered(_iter_relationship_user_ids_to_request(user_id, relationships))
    
    return _make_suggestions(users, value, guild_id)


async def get_relationship_and_user_like_at(user_id, value, guild_id):
    """
    Helper function for getting a single relationship and user with a name like the given one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who ising.
    
    value : `None | str`
        The value to get user name for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    relationship_and_user : `(Relationship, ClientUserBase)`
    
    Raises
    ------
    InteractionAbortedError
    """
    while True:
        if value is None:
            break
        
        relationships = await get_relationship_listing(user_id)
        if relationships is None:
            break
        
        users = await get_users_unordered(_iter_relationship_user_ids_to_request(user_id, relationships))
        
        relationship_and_user = _select_first_relationship_and_user(relationships, users, value, guild_id)
        if relationship_and_user is None:
            break
        
        return relationship_and_user
    
    abort('Could not match anyone.')


async def autocomplete_relationship_user_name(event, value):
    """
    Autocompletes a relationship's user name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value to auto complete.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    return await get_relationship_user_names_like_at(event.user_id, value, event.guild_id)


async def get_relationship_unset_outgoing_user_names_like_at(user_id, value, guild_id):
    """
    Helper function for auto completing outgoing unset relationship user names.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who ising.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    relationships = await get_relationship_listing(user_id)
    if relationships is None:
        return None
    
    relationships = _filter_relationships_unset_outgoing(user_id, relationships)
    if relationships is None:
        return None
    
    users = await get_users_unordered(_iter_relationship_user_ids_to_request(user_id, relationships))
    return _make_suggestions(users, value, guild_id)


async def get_relationship_unset_outgoing_and_user_like_at(user_id, value, guild_id):
    """
    Helper function for getting an unset outgoing relationship and single user with a name like the given one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who ising.
    
    value : `None | str`
        The value to get user name for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    relationship_and_user : `(Relationship, ClientUserBase)`
    
    Raises
    ------
    InteractionAbortedError
    """
    while True:
        if value is None:
            break
        
        relationships = await get_relationship_listing(user_id)
        if relationships is None:
            break
        
        relationships = _filter_relationships_unset_outgoing(user_id, relationships)
        if relationships is None:
            break
        
        users = await get_users_unordered(_iter_relationship_user_ids_to_request(user_id, relationships))
        
        relationship_and_user = _select_first_relationship_and_user(relationships, users, value, guild_id)
        if relationship_and_user is None:
            break
        
        return relationship_and_user
    
    abort('Could not match anyone.')


async def autocomplete_relationship_unset_outgoing_user_name(event, value):
    """
    Autocompletes an outgoing unset  relationship's user name.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value to auto complete.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    return await get_relationship_unset_outgoing_user_names_like_at(event.user_id, value, event.guild_id)


async def get_relationship_extended_user_names_like_at(user_id, value, guild_id):
    """
    Helper function for auto completing relationship user names of the user
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who ising.
    
    value : `None | str`
        The value to auto complete.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    relationship_listing, relationship_listing_extend = await get_relationship_listing_and_extend(user_id)
    if relationship_listing is None:
        return None
    
    users = await get_users_unordered(iter_relationship_and_extend_user_ids_to_request(
        user_id, relationship_listing, relationship_listing_extend
    ))
    
    return _make_suggestions(users, value, guild_id)


async def get_extender_relationship_and_relationship_and_user_like_at(user_id, value, guild_id):
    """
    Helper function for getting the director relationship for indirect relationships from the extended relationship
    listing and the single matched relationship and user with a name like the given one.
    
    This function is a coroutine.
    
    Parameters
    ----------
    user_id : `int`
        The user's identifier who ising.
    
    value : `None | str`
        The value to get user name for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    extender_relationship_and_relationship_and_user : `(None | Relationship, Relationship, ClientUserBase)`
    
    Raises
    ------
    InteractionAbortedError
    """
    while True:
        if value is None:
            break
        
        relationship_listing, relationship_listing_extend = await get_relationship_listing_and_extend(user_id)
        if relationship_listing is None:
            break
        
        users = await get_users_unordered(iter_relationship_and_extend_user_ids_to_request(
            user_id, relationship_listing, relationship_listing_extend
        ))
        
        extender_relationship_and_relationship_and_user = _select_first_extender_relationship_and_relationship_and_user(
            relationship_listing, relationship_listing_extend, users, value, guild_id
        )
        if extender_relationship_and_relationship_and_user is None:
            break
        
        return extender_relationship_and_relationship_and_user
    
    abort('Could not match anyone.')


async def autocomplete_relationship_extended_user_name(event, value):
    """
    Autocompletes a relationship's user name from the event's user's extended relationship listing.
    
    This function is a coroutine.
    
    Parameters
    ----------
    event : ``InteractionEvent``
        The received interaction event.
    
    value : `None | str`
        The value to auto complete.
    
    Returns
    -------
    suggestions : `None | list<str>`
    """
    return await get_relationship_extended_user_names_like_at(event.user_id, value, event.guild_id)
