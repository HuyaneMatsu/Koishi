__all__ = (
    'calculate_relationship_value', 'get_affinity_multiplier', 'get_affinity_percent', 'get_root', 'get_square',
    'iter_select_relationships', 'select_extender_relationship_and_relationship_for_user_id',
    'select_first_user_for_value', 'select_relationship', 'select_relationship_for_user_id',
)

from config import KOISHI_ID

from ...bot_utils.constants import RELATIONSHIP_VALUE_DEFAULT

from math import floor

from .completion_helpers import looks_like_user_id
from .relationship_types import RELATIONSHIP_TYPE_NONE, RELATIONSHIP_TYPE_RELATIONSHIPS


def get_affinity_percent(source_user_id, target_user_id):
    """
    Gets the love affinity between the two users.
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    Returns
    -------
    percent : `int`
    """
    if (source_user_id == KOISHI_ID) or (target_user_id == KOISHI_ID):
        return 100
    
    return ((source_user_id ^ target_user_id) >> 22) % 101


def get_affinity_multiplier(source_user_id, target_user_id):
    """
    Gets the relationship value multiplier between the two users.
    
    Parameters
    ----------
    source_user_id : `int`
        The source user's identifier.
    
    target_user_id : `int`
        The target user's identifier.
    
    Returns
    -------
    multiplier : `float`
    """
    return 2.1 - (get_affinity_percent(source_user_id, target_user_id) * 0.01)


def get_square(value):
    """
    Gets the square of the given value.
    
    Note: If `value` is negative returns a negative value.
    
    Parameters
    ----------
    value : `int`
        The value to square up.
    
    Returns
    -------
    value : `int`
    """
    output = value * value
    if value < 1:
        output = -output
    
    return output


def get_root(value):
    """
    Gets the square root of the given value.
    
    Note: If `value` is negative returns a negative value.
    
    Parameters
    ----------
    value : `int`
        The value to square up.
    
    Returns
    -------
    value : `int`
    """
    if value >= 0:
        negative = False
    
    else:
        negative = True
        value = -value
    
    output = value ** 0.5
    
    if negative:
        output = -output
    
    return floor(output)


def calculate_relationship_value(user_id, base_relationship_value, relationships):
    """
    Calculates the relationship's value for the given user.
    
    Parameters
    ----------
    user_id  : `int`
        The user's identifier.
    
    base_relationship_value : `int`
        The base value for the user's relationships.
    
    relationships : `None | list<Relationship>`
        The user's relationships.
    
    Returns
    -------
    relationship_value : `int`
    """
    relationship_value = base_relationship_value
    
    if (relationships is not None):
        cumulative = get_square(relationship_value)
        
        for relationship in relationships:
            if relationship.source_user_id == user_id:
                relationship_value = relationship.source_investment
            else:
                relationship_value = relationship.target_investment
            cumulative += get_square(relationship_value)
        
        relationship_value = get_root(cumulative)
    
    relationship_value = max(relationship_value, RELATIONSHIP_VALUE_DEFAULT)
    return relationship_value


def select_relationship(user_id, relationship_type, relationship_listing):
    """
    Gets the relationship from the given one under a condition.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to filter based on.
    
    relationship_type : `int`
        The relation type to look for.
    
    relationship_listing : `None | list<Relationship>`
        The relationships to select from.
    
    Returns
    -------
    relationship : `None | Relationship`
    """
    if relationship_listing is None:
        return None
    
    reversed_relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    
    for relationship in relationship_listing:
        if relationship.source_user_id == user_id:
            if relationship.relationship_type == reversed_relationship_type:
                return relationship
            continue
        
        if relationship.target_user_id == user_id:
            if relationship.relationship_type == relationship_type:
                return relationship
            continue
        
        # no more cases
        continue
    
    return None


def iter_select_relationships(user_id, relationship_type, relationship_listing):
    """
    Iterates over all the relationships matching the given type.
    
    This function is an iterable generator.
    
    Yields
    ------
    user_id : `int`
        The user identifier to filter based on.
    
    relationship_type : `int`
        The relation type to look for.
    
    relationship_listing : `None | list<Relationship>`
        The relationships to select from.
    
    Returns
    -------
    relationship : `None | Relationship`
    """
    if relationship_listing is None:
        return
    
    reversed_relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    
    for relationship in relationship_listing:
        if relationship.source_user_id == user_id:
            if relationship.relationship_type == reversed_relationship_type:
                yield relationship
            continue
        
        if relationship.target_user_id == user_id:
            if relationship.relationship_type == relationship_type:
                yield relationship
            continue
        
        # no more cases
        continue


def select_first_user_for_value(users, value, guild_id):
    """
    Selects the first matching user and returns it.
    
    Parameters
    ----------
    users : `list<ClientUserBase>`
        The users to filter from.
    
    value : `str`
        Value to filter for.
    
    guild_id : `int`
        The respective guild's identifier.
    
    Returns
    -------
    user : `None | ClientUserBase`
    """
    if looks_like_user_id(value):
        passed_user_id = int(value)
        
        for user in users:
            if user.id == passed_user_id:
                return user
    
    for user in users:
        if user.has_name_like_at(value, guild_id):
            return user


def select_relationship_for_user_id(relationship_listing, user_id):
    """
    Selects the first relationship with the given user identifier.
    
    Parameters
    ----------
    relationship_listing : `list<Relationship>`
        Relationships to select from.
    
    user_id : `int`
        The user identifier to select relationship with.
    
    Returns
    -------
    relationship : `None | Relationship`
    """
    for relationship in relationship_listing:
        if (relationship.source_user_id == user_id) or (relationship.target_user_id == user_id):
            return relationship


def select_extender_relationship_and_relationship_for_user_id(
    relationship_listing_with_extend, user_id
):
    """
    Selects the extender relationship and the relationship of the given user identifier.
    
    Parameters
    ----------
    relationship_listing_with_extend : `None | list<(Relationship, None | list<Relationship>)>`
        The relationship extends to get the user identifiers from.
    
    user_id : `int`
        The user identifier to select relationship with.
    
    Returns
    -------
    extender_relationship_and_relationship : `None | (None | Relationship, Relationship)`
    """
    if relationship_listing_with_extend is None:
        return None
    
    for extender_relationship, relationship_listing_extend in relationship_listing_with_extend:
        if (extender_relationship.source_user_id == user_id) or (extender_relationship.target_user_id == user_id):
            return None, extender_relationship
        
        if (relationship_listing_extend is None):
            continue
        
        relationship = select_relationship_for_user_id(relationship_listing_extend, user_id)
        if (relationship is not None):
            return extender_relationship, relationship
