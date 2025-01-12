__all__ = ('get_affinity_percent',)

from ...bot_utils.constants import RELATIONSHIP_VALUE_DEFAULT

from math import floor

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
    return ((source_user_id ^ target_user_id) & 0b1111111111111111111111) % 101


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


def select_relationship(user_id, relationship_type, relationships):
    """
    Gets the relationship from the given one under a condition.
    
    Parameters
    ----------
    user_id : `int`
        The user identifier to filter based on.
    
    relationship_type : `int`
        The relation type to look for.
    
    relationships : `None | list<Relationship>`
        The relationship types to get from.
    
    Returns
    -------
    relationship : `None | Relationship`
    """
    if relationships is None:
        return None
    
    reversed_relationship_type = RELATIONSHIP_TYPE_RELATIONSHIPS.get(relationship_type, RELATIONSHIP_TYPE_NONE)
    
    for relationship in relationships:
        if relationship.source_user_id == user_id:
            if relationship.relationship_type == relationship_type:
                return relationship
            continue
        
        if relationship.target_user_id == user_id:
            if relationship.relationship_type == reversed_relationship_type:
                return relationship
            continue
        
        # no more cases
        continue
    
    return None

